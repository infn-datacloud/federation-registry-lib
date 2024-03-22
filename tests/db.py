import re
from typing import Any, Dict
from uuid import uuid4

from neo4j.graph import Node

from fed_reg.flavor.models import Flavor
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.image.models import Image
from fed_reg.location.models import Location
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup

CLASS_DICT = {
    "Flavor": Flavor,
    "Identity_Provider": IdentityProvider,
    "Image": Image,
    "Location": Location,
    "Network": Network,
    "Project": Project,
    "Provider": Provider,
    "BlockStorageQuota": BlockStorageQuota,
    "ComputeQuota":ComputeQuota,
    "NetworkQuota": NetworkQuota,
    "Region": Region,
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
        print(query, kwargs)

        # Detect if it is a CREATE request.
        match = re.search(r"(?<=CREATE\s\(n\:)\w+(?=\s|\:)", query)
        if match is not None:
            item_type = match.group(0)
            return self.create(item_type, params)

        # Detect if it is a MATCH request
        match = re.search(r"(?<=MATCH\s\()\w+(?=\))", query)
        if match is not None:
            item_type = match.group(0).capitalize()
            match = re.search(r"(?<=RETURN\s)\w+(?=$|\s)", query)
            if match is not None:
                node_name = match.group(0)
                return self.match(
                    item_type,
                    node_name,
                    query,
                    resolve_objects=kwargs.get("resolve_objects", False)
                    )
            match = re.search(r"(?<=MERGE.).*$", query)
            if match is not None:
                return self.merge(params, match.group(0))


    def create(self, item_type, params):
        element_id = f"{self.db_version}:{uuid4().hex}:{self.count}"
        item = Node(
            ...,
            element_id=element_id,
            id_=self.count,
            properties=params["create_params"],
        )
        self.data[item_type] = [item]
        self.count += 1
        return [[i] for i in self.data[item_type]], None


    def match(self, src_type, node_name, query, resolve_objects):
        if src_type not in node_name:
            idx = node_name.rfind("_")
            if idx > -1:
                rel_name = node_name[idx+1:]
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
        match = re.search(r"(?<=\`).*(?=\`)", query)
        relationship = match.group(0)
        if self.data.get(relationship):
            self.data[relationship].append(params)
        else:
            self.data[relationship] = [params]
