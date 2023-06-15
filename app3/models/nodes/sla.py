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
from ..relationships import Project, Quota


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

    user_group = RelationshipFrom(".UserGroup", "HAS_SLA", cardinality=One)
    provider = RelationshipTo(
        ".Provider",
        "ACCESS_PROVIDER_THROUGH_PROJECT",
        cardinality=One,
        model=Project,
    )
    services = RelationshipTo(
        ".Service",
        "USE_SERVICE_WITH_QUOTA",
        cardinality=OneOrMore,
        model=Quota,
    )
