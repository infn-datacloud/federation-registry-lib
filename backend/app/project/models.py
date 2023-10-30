from typing import List

from app.flavor.models import Flavor
from app.image.models import Image
from app.network.models import Network
from neomodel import (
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
    ZeroOrOne,
)


class Project(StructuredNode):
    """Project owned by a Provider.

    A project/tenant/namespace is uniquely identified in the
    Provider by its uuid.
    It has a name and can access all public flavors, images
    and networks plus the private flavors, images and networks.
    It has a set of quotas limiting the resources it can use on
    a specific service of the hosting Provider.
    A project should always be pointed by an SLA.

    Attributes:
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    uuid = StringProperty(required=True)

    sla = RelationshipFrom(
        "..sla.models.SLA",
        "REFER_TO",
        cardinality=ZeroOrOne,
    )
    quotas = RelationshipTo(
        "..quota.models.Quota",
        "USE_SERVICE_WITH",
        cardinality=ZeroOrMore,
    )
    provider = RelationshipFrom(
        "..provider.models.Provider",
        "BOOK_PROJECT_FOR_SLA",
        cardinality=One,
    )
    private_flavors = RelationshipTo(
        "..flavor.models.Flavor",
        "CAN_USE_VM_FLAVOR",
        cardinality=ZeroOrMore,
    )
    private_images = RelationshipTo(
        "..image.models.Image",
        "CAN_USE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
    private_networks = RelationshipTo(
        "..network.models.Network",
        "CAN_USE_NETWORK",
        cardinality=ZeroOrMore,
    )

    query_prefix = """
        MATCH (p:Project)
        WHERE (id(p)=$self)
        MATCH (p)-[:USE_SERVICE_WITH]-(q)
        WHERE q.type = compute
        MATCH (q)-[:APPLY_TO]-(s)
        """

    def public_flavors(self) -> List[Flavor]:
        results, columns = self.cypher(
            f"""
                {self.query_prefix}
                MATCH (s)-[:AVAILABLE_VM_FLAVOR]->(u)
                WHERE u.is_public = True
                RETURN u
            """
        )
        return [Flavor.inflate(row[0]) for row in results]

    def public_images(self) -> List[Image]:
        results, columns = self.cypher(
            f"""
                {self.query_prefix}
                MATCH (s)-[:AVAILABLE_VM_IMAGE]->(u)
                WHERE u.is_public = True
                RETURN u
            """
        )
        return [Image.inflate(row[0]) for row in results]

    def public_networks(self) -> List[Network]:
        results, columns = self.cypher(
            f"""
                {self.query_prefix}
                MATCH (s)-[:SUPPLY]-(r)
                MATCH (r)-[:SUPPLY]-(n)
                WHERE n.type = network
                MATCH (n)-[:AVAILABLE_NETWORK]->(u)
                WHERE u.is_shared = True
                RETURN u
            """
        )
        return [Network.inflate(row[0]) for row in results]
