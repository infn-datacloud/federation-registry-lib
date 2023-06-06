from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    RelationshipFrom,
    RelationshipTo,
    One,
    ZeroOrMore,
)


class Project(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")

    user_group = RelationshipFrom(
        ".UserGroup", "HAS_ACCESS_TO", cardinality=One
    )
    flavors = RelationshipTo(
        ".Flavor", "AVAILABLE_VM_SIZE", cardinality=ZeroOrMore
    )
    images = RelationshipTo(
        ".Image", "AVAILABLE_VM_IMAGE", cardinality=ZeroOrMore
    )
