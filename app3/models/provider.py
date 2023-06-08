from neomodel import (
    ArrayProperty,
    BooleanProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
    ZeroOrOne,
)


class Provider(StructuredNode):
    """Provider class.

    A Provider has a list of maintainers, can be public
    and has a geographical localization. It support a set
    of images and flavors. It is involved in a set of SLA
    allowing user groups to access its own resources.

    Attributes:
        uid (int): Provider unique ID.
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")
    is_public = BooleanProperty(default=False)
    support_email = ArrayProperty(StringProperty())

    projects = RelationshipFrom(
        ".UserGroup", "ASSOCIATED_PROJECT_ON", cardinality=ZeroOrMore
    )
    flavors = RelationshipFrom(
        ".Flavor", "SUPPORTED_VM_SIZE", cardinality=ZeroOrMore
    )
    images = RelationshipFrom(
        ".Image", "SUPPORTED_VM_IMAGE", cardinality=ZeroOrMore
    )
    slas = RelationshipTo(
        ".SLA", "RESOURCES_RETRIEVED_FROM", cardinality=ZeroOrMore
    )
    location = RelationshipTo(".Location", "LOCATED_AT", cardinality=ZeroOrOne)
