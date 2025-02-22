"""Neomodel model of the Project owned by a Provider."""
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

from fedreg.flavor.models import Flavor
from fedreg.image.models import Image
from fedreg.network.models import Network
from fedreg.service.enum import ServiceType
from fedreg.sla.models import SLA


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
    ----------
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
        "fedreg.sla.models.SLA",
        "REFER_TO",
        cardinality=ZeroOrOne,
    )
    quotas = RelationshipTo(
        "fedreg.quota.models.Quota",
        "USE_SERVICE_WITH",
        cardinality=ZeroOrMore,
    )
    provider = RelationshipFrom(
        "fedreg.provider.models.Provider",
        "BOOK_PROJECT_FOR_SLA",
        cardinality=One,
    )
    private_flavors = RelationshipTo(
        "fedreg.flavor.models.Flavor",
        "CAN_USE_VM_FLAVOR",
        cardinality=ZeroOrMore,
    )
    private_images = RelationshipTo(
        "fedreg.image.models.Image",
        "CAN_USE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
    private_networks = RelationshipTo(
        "fedreg.network.models.Network",
        "CAN_USE_NETWORK",
        cardinality=ZeroOrMore,
    )

    query_prefix = """
        MATCH (p:Project)
        WHERE (elementId(p)=$self)
        MATCH (p)-[:`USE_SERVICE_WITH`]-(q)
        """

    def public_flavors(self) -> list[Flavor]:
        """list public flavors this project can access.

        Make a cypher query to retrieve all public flavors this project can access.
        """
        results, _ = self.cypher(
            f"""
                {self.query_prefix}
                WHERE q.type = "{ServiceType.COMPUTE.value}"
                MATCH (q)-[:`APPLY_TO`]-(s)
                MATCH (s)-[:`AVAILABLE_VM_FLAVOR`]->(u:Flavor)
                WHERE u.is_public = True
                RETURN u
            """
        )
        return [Flavor.inflate(row[0]) for row in results]

    def public_images(self) -> list[Image]:
        """list public images this project can access.

        Make a cypher query to retrieve all public images this project can access.
        """
        results, _ = self.cypher(
            f"""
                {self.query_prefix}
                WHERE q.type = "{ServiceType.COMPUTE.value}"
                MATCH (q)-[:`APPLY_TO`]-(s)
                MATCH (s)-[:`AVAILABLE_VM_IMAGE`]->(u:Image)
                WHERE u.is_public = True
                RETURN u
            """
        )
        return [Image.inflate(row[0]) for row in results]

    def public_networks(self) -> list[Network]:
        """list public networks this project can access.

        Make a cypher query to retrieve all public networks this project can access.
        """
        results, _ = self.cypher(
            f"""
                {self.query_prefix}
                WHERE q.type = "{ServiceType.NETWORK.value}"
                MATCH (q)-[:`APPLY_TO`]-(s)
                MATCH (s)-[:`AVAILABLE_NETWORK`]->(u:Network)
                WHERE u.is_shared = True
                RETURN u
            """
        )
        return [Network.inflate(row[0]) for row in results]

    def pre_delete(self):
        """Remove related quotas and SLA.

        Remove the SLA only if that SLA points only to this project.
        """
        for item in self.quotas:
            item.delete()
        item: SLA = self.sla.single()
        if item and len(item.projects) == 1:
            item.delete()
