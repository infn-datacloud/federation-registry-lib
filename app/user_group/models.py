from typing import List
from neomodel import (
    One,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)

from ..cluster.models import Cluster
from ..flavor.models import Flavor
from ..image.models import Image
from ..service.models import Service
from ..service.schemas_extended import ServiceExtended
from ..service_type.enum import ServiceType as ServiceTypeEnum


class UserGroup(StructuredNode):
    """User Group class.

    Node containing the user group name and a brief description.
    A UserGroup has access to a set of images and flavors. It
    has access for each provider to only one project. For each
    provider it can have a SLA defining the services and the
    resources it can access.

    Attributes:
        name (str): UserGroup name.
        description (str): Brief description.
    """

    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty(default="")

    projects = RelationshipTo(
        "..project.models.PROJECT", "MATCH_PROJECT", cardinality=ZeroOrMore
    )
    identity_provider = RelationshipTo(
        "..identity_provider.models.IdentityProvider",
        "BELONGS_TO",
        cardinality=One,
    )

    query_srv_prefix = """
        MATCH (g:UserGroup)
        WHERE (id(g)=$self)
        MATCH (g)-[:HAS_SLA]->(x)-[:USE_SERVICE_WITH_QUOTA]->(q)
        MATCH (q)-[:APPLIES_TO]->(s)
        """

    query_srv_body = """
        MATCH (s)-[:HAS_TYPE]->(st)
        WHERE (st.name=$service)
        MATCH (s)<-[:PROVIDES_SERVICE]-(p)
    """

    def clusters(self) -> List[Cluster]:
        results, columns = self.cypher(
            f"""
                {self.query_srv_prefix}
                {self.query_srv_body}
                MATCH (p)-[:AVAILABLE_CLUSTER]->(u)
                RETURN u
            """,
            {"service": ServiceTypeEnum.kubernetes.value},
        )
        return [Cluster.inflate(row[0]) for row in results]

    def flavors(self) -> List[Flavor]:
        results, columns = self.cypher(
            f"""
                {self.query_srv_prefix}
                {self.query_srv_body}
                MATCH (p)-[:AVAILABLE_VM_FLAVOR]->(u)
                RETURN s
            """,
            {"service": ServiceTypeEnum.open_stack_nova.value},
        )
        print(results)
        return [Flavor.inflate(row[0]) for row in results]

    def images(self) -> List[Image]:
        results, columns = self.cypher(
            f"""
                {self.query_srv_prefix}
                {self.query_srv_body}
                MATCH (p)-[:AVAILABLE_VM_IMAGE]->(u)
                RETURN u
            """,
            {"service": ServiceTypeEnum.open_stack_nova.value},
        )
        return [Image.inflate(row[0]) for row in results]

    def services(self) -> List[ServiceExtended]:
        results, columns = self.cypher(
            f"""
            {self.query_srv_prefix}
            RETURN s
        """
        )

        services = {}
        for row in results:
            service = Service.inflate(row[0])
            if service.uid not in services.keys():
                services[service.uid] = service
        return list(services.values())
