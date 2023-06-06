from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    RelationshipFrom,
    One,
)


class Project(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")

    user_group = RelationshipFrom(
        ".UserGroup", "HAS_ACCESS_TO", cardinality=One
    )
