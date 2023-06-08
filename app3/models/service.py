from neomodel import (
    ArrayProperty,
    BooleanProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class Service(StructuredNode):
    """Service class.

    A Service manages a specific amount of resource types
    defined by a set of quotas and belonging to an SLA.
    It is accessible through an endpoint. Authentication
    through IAM can be accepted. It can accept multiple
    authentication methods. It can be public or private.

    Attributes:
        uid (int): Service unique ID.
        name (str): Service name (type).
        description (str): Brief description.
        resource_type (str): Resource type.
        endpoint (str): URL pointing to this service
        iam_enabled (bool): IAM enabled for this service.
        is_public (bool): Public Service or not.
        public_ip_assignable (bool): It is possible to
            assign a public IP to this service.
        volume_types (list of str): TODO
    """

    uid = UniqueIdProperty()
    name = StringProperty(required=True)  # TODO Add choices.
    description = StringProperty(default="")
    resource_type = StringProperty(required=True)  # TODO Add choices.
    endpoint = StringProperty(required=True)
    iam_enabled = BooleanProperty(default=False)
    is_public = BooleanProperty(default=False)
    public_ip_assignable = BooleanProperty(default=False)
    volume_types = ArrayProperty(StringProperty())

    sla = RelationshipFrom(".SLA", "RESOURCES_MANAGED_BY", cardinality=One)
    idps = RelationshipTo(
        ".IdentityProvider", "AUTHENTICATES_THROUGH", cardinality=ZeroOrMore
    )
    quotas = RelationshipFrom(
        ".Quota", "APPLIED_RESOURCE_RESTRICTION", cardinality=ZeroOrMore
    )
