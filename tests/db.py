import re
from typing import Any
from uuid import uuid4

import networkx as nx
from neo4j.graph import Node, Relationship

from fed_reg.flavor.models import Flavor
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.image.models import Image
from fed_reg.location.models import Location
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota, Quota
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    Service,
)
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup

CLASS_DICT = {
    "Flavor": Flavor,
    "IdentityProvider": IdentityProvider,
    "Image": Image,
    "Location": Location,
    "Network": Network,
    "Project": Project,
    "Provider": Provider,
    "Quota": Quota,
    "BlockStorageQuota": BlockStorageQuota,
    "ComputeQuota": ComputeQuota,
    "NetworkQuota": NetworkQuota,
    "Region": Region,
    "Service": Service,
    "BlockStorageService": BlockStorageService,
    "ComputeService": ComputeService,
    "IdentityService": IdentityService,
    "NetworkService": NetworkService,
    "SLA": SLA,
    "UserGroup": UserGroup,
}


class MockDatabase:
    def __init__(self, db_version: int = 5) -> None:
        self.db_version = db_version
        self.graph = nx.Graph()
        self.count = 0

    def query_call(self, query: str, params: dict[str, Any], **kwargs):
        # print(query, params, kwargs)
        resolve_objects = kwargs.get("resolve_objects", False)

        # Detect if it is a CREATE request.
        match = re.search(r"(?<=CREATE\s\(n\:)[\w\:]+(?=\s)", query)
        if match is not None:
            item_type = match.group(0)
            data = params["create_params"]
            return self.create(item_type=item_type, data=data)

        # Detect if it is a MATCH request
        match = re.search(r"(?<=MATCH\s\()\S+(?=\))", query)
        if match is not None:
            if ":" in match.group(0):
                item_name, item_type = match.group(0).split(":")
            else:
                item_type = match.group(0).capitalize()
                item_name = None

            # Detect if it is a MERGE request (connect)
            match = re.search(r"(?<=MERGE.).*$", query)
            if match is not None:
                match = re.search(r"(?<=\`).*(?=\`)", match.group(0))
                rel_type = match.group(0)
                start_node, end_node = self._get_start_end_nodes(params)
                exclude_keys = {"self", "them"}
                data = {k: params[k] for k in set(params.keys()) - exclude_keys}
                return self.connect(
                    start_node=start_node,
                    end_node=end_node,
                    rel_type=rel_type,
                    data=data,
                )

            # Detect return type
            match = re.search(r"(?<=RETURN\s)[^\s]+(?=$|\s)", query)
            if match is not None:
                return_string = match.group(0)
                # Return nodes of `item_type`.
                if item_name == return_string:
                    return self.get_nodes(item_type, return_string, resolve_objects)

                start_node = self._get_start_node(params)
                if start_node is not None:
                    match = re.search(r"(?<=count\()\w+(?=\))", return_string)
                    # Return the number of related nodes
                    if match is not None:
                        return self.count_related_nodes(
                            start_node=start_node,
                            return_string=match.group(0),
                            query=query,
                        )
                    # Return related nodes
                    if item_type not in return_string:
                        rel_string = return_string.rsplit("_", 1)[-1]
                        return self.get_relationships(
                            start_node=start_node,
                            rel_string=rel_string,
                            return_string=return_string,
                            query=query,
                            resolve_objects=resolve_objects,
                        )

                else:
                    return [], None

    def connect(self, *, start_node, end_node, rel_type, data):
        """
        Connect 2 nodes.

        With normal relationships return nothing.
        If in the params dict there are other keys other then them and self, the
        relationship stores additional data; in that case set the start and end node
        of the relationship and return it.
        """
        rel = None
        if data:
            element_id = f"{self.db_version}:{uuid4().hex}:{self.count}"
            rel = Relationship(
                ..., element_id=element_id, id_=self.count, properties=data
            )
            rel._start_node = start_node
            rel._end_node = end_node
        self.graph.add_edge(start_node, end_node, data=rel, labels=rel_type.split(":"))
        return [[rel]], ["r"]

    def count_related_nodes(self, *, start_node, return_string, query):
        """
        Count neighbors nodes

        Detect from the return string the type of the neighbors.
        """
        if return_string.rfind("_") > -1:
            match = re.search(rf"(?<={return_string}:)\w+(?=\))", query)
            dest_type = match.group(0)
            relationships = self._get_related_nodes(start_node, dest_type)
            return [[len(relationships)]], [return_string]

    def create(self, *, item_type, data) -> tuple[list[list[Node]], None]:
        """
        Create a node element with the given parameters.

        Store the node in the graph. `labels` attribute contains the list of the neo4j
        labels matching this item.
        """
        element_id = f"{self.db_version}:{uuid4().hex}:{self.count}"
        item = Node(
            ...,
            element_id=element_id,
            id_=self.count,
            properties={**data, "element_id_property": element_id},
        )
        self.graph.add_node(item, labels=item_type.split(":"))
        self.count += 1
        return [[item]], None

    def get_relationships(
        self, *, start_node, rel_string, return_string, query, resolve_objects
    ):
        """
        Retrieve related nodes or relationships from a given node.

        If `dest_type` is defined, then return the related nodes, otherwise return the
        relationships.
        """
        match = re.search(rf"(?<={return_string}:)\w+(?=\))", query)
        if match is not None:
            dest_type = match.group(0)
            relationships = self._get_related_nodes(
                start_node, dest_type, resolve_objects
            )
        else:
            match = re.search(rf"(?<={rel_string}:\`)\w+(?=\`)", query)
            rel_type = match.group(0)
            relationships = self._get_related_edges(start_node, rel_type)
        return relationships, [return_string]

    def get_nodes(self, item_type, return_string, resolve_objects):
        nodes = filter(lambda x: item_type in x[1], self.graph.nodes.data("labels"))
        nodes = [i[0] for i in nodes]
        if resolve_objects:
            nodes = [[CLASS_DICT[item_type](**i)] for i in nodes]
        return nodes, [return_string]

    def _get_start_end_nodes(self, params):
        """
        Search in the graph the start and end nodes.

        Start node match the `self` attribute in the params dictionary.
        End node match the `them` attribute in the params dictionary.
        """
        for node in self.graph.nodes:
            if node.element_id == params.get("self"):
                start_node = node
            if node.element_id == params.get("them"):
                end_node = node
        return start_node, end_node

    def _get_start_node(self, params):
        """
        Search the node matching the id in the params dictionary.
        """
        target_id = params.get("self", None)
        if not target_id:
            target_id = next(iter(params.values()))
        for node in self.graph.nodes:
            if node.element_id == target_id:
                return node

    def _get_related_nodes(self, start_node, dest_type, resolve_objects=False):
        """
        Get neighbors of a given node.

        Inflate nodes type if `resolve_objects` is true.
        """
        relationships = filter(
            lambda x: dest_type in self.graph.nodes[x]["labels"],
            self.graph.neighbors(start_node),
        )
        if resolve_objects:
            return [[CLASS_DICT[dest_type](**i)] for i in relationships]
        return [[i] for i in relationships]

    def _get_related_edges(self, start_node, rel_type):
        """
        Get neighbors of a given node.

        Inflate nodes type if `resolve_objects` is true.
        """
        relationships = filter(
            lambda x: rel_type in x[2]["labels"],
            self.graph.edges(start_node, data=True),
        )
        return [[rel[2]["data"]] for rel in relationships]
