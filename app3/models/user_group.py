from neomodel import StructuredNode, UniqueIdProperty, StringProperty


class UserGroup(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")
    # slas: List[SLA] = Field(default_factory=list)
