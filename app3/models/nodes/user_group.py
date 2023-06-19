from typing import List, Tuple
from neomodel import (
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)

from .cluster import Cluster
from .flavor import Flavor
from .image import Image
from .service import Service
from ..relationships import Quota, ProvideService
from ...schemas.utils import ServiceType


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
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")

    slas = RelationshipTo(".SLA", "HAS_SLA", cardinality=ZeroOrMore)

    query_srv_prefix = """
        MATCH (p:UserGroup) 
        WHERE (id(p)=$self) 
        MATCH (p)-[:HAS_SLA]->(q)-[r:USE_SERVICE_WITH_QUOTA]->(s)
        """

    def clusters(self) -> List[Cluster]:
        results, columns = self.cypher(
            f"""
                {self.query_srv_prefix}
                WHERE (s.name=$service)
                MATCH (s)-[:PROVIDES_SERVICE]->(t)-[:AVAILABLE_CLUSTER]->(u) 
                RETURN u
            """,
            {"service": ServiceType.kubernetes.value},
        )
        return [Cluster.inflate(row[0]) for row in results]

    def flavors(self) -> List[Flavor]:
        results, columns = self.cypher(
            f"""
                {self.query_srv_prefix}
                WHERE (s.name=$service)
                MATCH (s)-[:PROVIDES_SERVICE]->(t)-[:AVAILABLE_VM_SIZE]->(u) 
                RETURN u
            """,
            {"service": ServiceType.open_stack_nova.value},
        )
        return [Flavor.inflate(row[0]) for row in results]

    def images(self) -> List[Image]:
        results, columns = self.cypher(
            f"""
                {self.query_srv_prefix}
                WHERE (s.name=$service)
                MATCH (s)-[:PROVIDES_SERVICE]->(t)-[:AVAILABLE_VM_IMAGE]->(u) 
                RETURN u
            """,
            {"service": ServiceType.open_stack_nova.value},
        )
        return [Image.inflate(row[0]) for row in results]

    def services(self) -> List[Tuple[Service, ProvideService, List[Quota]]]:
        results, columns = self.cypher(
            f"""
                MATCH (p:UserGroup)-[:HAS_SLA]->(q)
                WHERE p.uid="e49648ce4068463ca4d54ab2e8a8ecce"
                MATCH (a)<-[b:BOOK_PROJECT_FOR_AN_SLA]->(c)
                    <-[d:ACCESS_PROVIDER_THROUGH_PROJECT]-(q)
                    -[r:USE_SERVICE_WITH_QUOTA]->(s)
                    -[t:PROVIDES_SERVICE]->(u) 
                WHERE a.uid = u.uid
                RETURN s, t, r
            """
        )
        services = []
        for row in results:
            service = Service.inflate(row[0])
            prov_details = ProvideService.inflate(row[1])
            quotas = []
            quotas.append(Quota.inflate(row[2]))  # TODO multiple quotas?
            services.append((service, prov_details, quotas))
        return services
