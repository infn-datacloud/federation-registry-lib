from neomodel import (
    DateProperty,
    One,
    OneOrMore,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
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
        doc_uuid (UUID): UUID of the document with
            the SLA details
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    start_date = DateProperty(required=True)
    end_date = DateProperty(required=True)
    doc_uuid = StringProperty()

    user_group = RelationshipFrom(
        "..user_group.models.UserGroup", "AGREE", cardinality=One
    )
    projects = RelationshipTo(
        "..project.models.Project", "REFER_TO", cardinality=OneOrMore
    )
