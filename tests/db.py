import re
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

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
        self.data = {}
        self.count = 0

    def query_call(self, query: str, params: Dict[str, Any], **kwargs):
        # print(query, kwargs)

        # Detect if it is a CREATE request.
        match = re.search(r"(?<=CREATE\s\(n\:)[\w\:]+(?=\s)", query)
        if match is not None:
            item_type = match.group(0)
            return self.create(item_type, params)

        # Detect if it is a MATCH request
        match = re.search(r"(?<=MATCH\s\()\w+(?=\))", query)
        if match is not None:
            item_type = match.group(0).capitalize()

            # Detect if it is a MERGE request (connect)
            match = re.search(r"(?<=MERGE.).*$", query)
            if match is not None:
                return self.merge(params, match.group(0))

            # Detect return type
            match = re.search(r"(?<=RETURN\s)[^\s]+(?=$|\s)", query)
            if match is not None:
                node_name = match.group(0)
                return self.match(
                    item_type,
                    node_name,
                    query,
                    resolve_objects=kwargs.get("resolve_objects", False),
                )

    def create(self, item_type, params) -> Tuple[List[List[Node]], None]:
        """
        Create a node element with the given parameters.

        Save the node in the class' dict. The key to use is the received label.
        Each label stores a list of nodes.
        When receiving multiple labels, create the node once and add it to each list.
        """
        element_id = f"{self.db_version}:{uuid4().hex}:{self.count}"
        item = Node(
            ...,
            element_id=element_id,
            id_=self.count,
            properties=params["create_params"],
        )
        self.count += 1
        for t in item_type.split(":"):
            if not self.data.get(t, None):
                self.data[t] = []
            self.data[t].append(item)
        return [[item]], None

    def match(self, src_type, node_name, query, resolve_objects):
        match = re.search(r"(?<=count\()\w+(?=\))", node_name)
        if match is not None:
            node_name = match.group(0)
            idx = node_name.rfind("_")
            if idx > -1:
                rel_name = node_name[idx + 1 :]
                match = re.search(rf"(?<={rel_name}:\`)\w+(?=\`)", query)
                rel_type = match.group(0)
                match = re.search(rf"(?<={node_name}:)\w+(?=\))", query)
                dest_type = match.group(0)
                relationships = self.get_related_items(
                    rel_type, dest_type, resolve_objects
                )
            return [[len(relationships)]], None

        if src_type not in node_name:
            idx = node_name.rfind("_")
            if idx > -1:
                rel_name = node_name[idx + 1 :]
                match = re.search(rf"(?<={rel_name}:\`)\w+(?=\`)", query)
                rel_type = match.group(0)
                match = re.search(rf"(?<={node_name}:)\w+(?=\))", query)
                dest_type = match.group(0)
                relationships = self.get_related_items(
                    rel_type, dest_type, resolve_objects
                )
                return relationships, [rel_type]
        return [[i] for i in self.data[src_type]], None

    def get_related_items(self, rel_type, dest_type, resolve_objects):
        relationships = []
        for i in self.data.get(dest_type, []):
            for j in self.data.get(rel_type, []):
                if j.get("them") == i.element_id:
                    if resolve_objects:
                        relationships += [[CLASS_DICT[dest_type](**i)]]
                    else:
                        relationships += [i]
        return relationships

    def merge(self, params, query):
        """
        Connect 2 nodes.

        With normal relationships return nothing.
        If in the params dict there are other keys other then them and self, the
        relationship stores additional data; in that case set the start and end node
        of the relationship and return it.
        """
        rel = None
        match = re.search(r"(?<=\`).*(?=\`)", query)
        relationship = match.group(0)

        data = {**params}
        data.pop("them", None)
        data.pop("self", None)

        if data:
            element_id = f"{self.db_version}:{uuid4().hex}:{self.count}"
            rel = Relationship(
                ...,
                element_id=element_id,
                id_=self.count,
                properties=data,
            )
            rel._start_node = self.search_node(params.get("self"))
            rel._end_node = self.search_node(params.get("them"))

        if self.data.get(relationship):
            self.data[relationship].append(params)
        else:
            self.data[relationship] = [params]
        return [[rel]], ["r"]

    def search_node(self, element_id) -> Optional[Node]:
        """
        When the node label is not specified, search in all nodes.

        Return the node with the given element_id otherwise return None.
        """
        for v in self.data.values():
            for i in filter(lambda x: isinstance(x, Node), v):
                if i.element_id == element_id:
                    return i
