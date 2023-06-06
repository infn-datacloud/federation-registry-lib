from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    RelationshipTo,
    ZeroOrMore,
)


class UserGroup(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")

    projects = RelationshipTo(
        ".Project", "HAS_ACCESS_TO", cardinality=ZeroOrMore
    )
