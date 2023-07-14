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
    """Associated Project class.

    Relationship linking a user group to a provider.
    This link correspond to a "project/tenant" entity.

    Attributes:
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        public_network_name (str): TODO
        private_network_name (str): TODO
        private_network_proxy_host (str): TODO
        private_network_proxy_user (str): TODO
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
    public_network_name = StringProperty()
    private_network_name = StringProperty()
    private_network_proxy_host = StringProperty()
    private_network_proxy_user = StringProperty()

    user_group = RelationshipFrom(
        "..user_group.models.UserGroup", "COUPLED_WITH", cardinality=ZeroOrOne
    )
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
    flavors = RelationshipTo(
        "..flavor.models.Flavor",
        "CAN_USE_VM_FLAVOR",
        cardinality=ZeroOrMore,
    )
    images = RelationshipTo(
        "..image.models.Image",
        "CAN_USE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
