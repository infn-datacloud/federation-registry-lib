"""Neomodel model of the Service Level Agreement between a Project and a User Group."""
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
    """Service Level Agreement between a Project and a User Group.

    An SLA defines the services and the resources a single User Group can use on
    one or multiple providers. Usually it is a document signed by the
    user group leader and
    the site admin.
    An SLA has a start and end date (which must be greater then the start date).

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    start_date = DateProperty(required=True)
    end_date = DateProperty(required=True)
    doc_uuid = StringProperty(required=True)

    user_group = RelationshipFrom(
        "..user_group.models.UserGroup", "AGREE", cardinality=One
    )
    projects = RelationshipTo(
        "..project.models.Project", "REFER_TO", cardinality=OneOrMore
    )
