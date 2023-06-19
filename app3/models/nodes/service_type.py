from neomodel import (
    OneOrMore,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class ServiceType(StructuredNode):
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
    description = StringProperty(default="")
    name = StringProperty(unique_index=True, required=True)

    service = RelationshipFrom(".Service", "HAS_TYPE", cardinality=ZeroOrMore)
    quota_types = RelationshipTo(
        ".QuotaType", "AVAILABLE_QUOTA_TYPE", cardinality=OneOrMore
    )
