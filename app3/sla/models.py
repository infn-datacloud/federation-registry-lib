from neomodel import (
    DateTimeProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    OneOrMore,
)


class SLA(StructuredNode):
    """Service Level Agreement class.

    A SLA has a start and end date. It defines the
    services a user group can use when accessing to
    a specific provider resources.

    Attributes:
        uid (int): SLA unique ID.
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    start_date = DateTimeProperty(required=True)
    end_date = DateTimeProperty(required=True)

    user_group = RelationshipFrom("..user_group.models.UserGroup", "HAS_SLA", cardinality=One)
    project = RelationshipTo(
        "..project.models.Project",
        "ACCESS_PROVIDER_THROUGH_PROJECT",
        cardinality=One,
    )
    quotas = RelationshipTo(
        "..quota.models.Quota", "USE_SERVICE_WITH_QUOTA", cardinality=OneOrMore
    )
