from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    FloatProperty,
    RelationshipFrom,
    One,
)


class Quota(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty(default="")
    tot_limit = FloatProperty(required=True)
    instance_limit = FloatProperty(required=True)
    user_limit = FloatProperty(required=True)
    tot_guaranteed = FloatProperty(default=0)
    instance_guaranteed = FloatProperty(default=0)
    user_guaranteed = FloatProperty(default=0)
    unit = StringProperty()

    sla = RelationshipFrom(
        ".SLA", "HAS_RESOURCE_RESTRICTIONS", cardinality=One
    )
