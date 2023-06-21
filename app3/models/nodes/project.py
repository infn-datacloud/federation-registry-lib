from neomodel import (
    One,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrOne,
)

from ..relationships import BookProject


class Project(StructuredNode):
    """Associated Project class.

    Relationship linking a user group to a provider.
    This link correspond to a "project/tenant" entity.

    Attributes:
        uid (uuid): AssociatedProject unique ID.
        project_name (str): Name of the project in the
            Provider to which this UserGroup has access.
        project_id (uuid): Project Unique ID in the Provider.
        public_network_name (str): #TODO
        private_network_name (str): #TODO
        private_network_proxy_name (str): #TODO
        private_network_proxy_host (str): #TODO
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    public_network_name = StringProperty()
    private_network_name = StringProperty()
    private_network_proxy_host = StringProperty()
    private_network_proxy_user = StringProperty()

    sla = RelationshipFrom(
        ".SLA", "ACCESS_PROVIDER_THROUGH_PROJECT", cardinality=ZeroOrOne
    )
    provider = RelationshipFrom(
        ".Provider",
        "BOOK_PROJECT_FOR_AN_SLA",
        cardinality=One,
        model=BookProject,
    )
