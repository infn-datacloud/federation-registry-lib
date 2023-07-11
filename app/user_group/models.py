from typing import List
from neomodel import (
    One,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)

from ..service.models import Service


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
        "..project.models.Project", "MATCH_PROJECT", cardinality=ZeroOrMore
    )
    flavors = RelationshipTo(
        "..flavor.models.Flavor", "CAN_USE_FLAVOR", cardinality=ZeroOrMore
    )
    images = RelationshipTo(
        "..image.models.Image", "CAN_USE_IMAGE", cardinality=ZeroOrMore
    )
    identity_provider = RelationshipTo(
        "..identity_provider.models.IdentityProvider",
        "BELONG_TO",
        cardinality=One,
    )

    query_prefix = """
        MATCH (g:UserGroup)
        WHERE (id(g)=$self)
        MATCH (g)-[:MATCH_PROJECT]->(p)
        """

    def services(self) -> List[Service]:
        results, columns = self.cypher(
            f"""
                {self.query_prefix}
                MATCH (p)-[:USE_SERVICE_WITH_QUOTA]->(q)-[:APPLIES_TO]->(s)
                RETURN s
            """
        )
        return [Service.inflate(row[0]) for row in results]
#        services = {}
#        for row in results:
#            service = Service.inflate(row[0])
#            if service.uid not in services.keys():
#                services[service.uid] = service
#        return list(services.values())
