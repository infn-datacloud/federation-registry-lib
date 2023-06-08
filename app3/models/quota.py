from neomodel import (
    FloatProperty,
    One,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class Quota(StructuredNode):
    """Quota class.

    A Quota defines the maximum quantity and the guaranteed
    quantity of a resource for a specific service.

    Attributes:
        uid (int): Quota unique ID.
        name (str): Quota name (type).
        description (str): Brief description.
        unit (str | None): Measurement unit derived from the
            quota name/type.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total.
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance.
        user_limit (float | None): The max quantity of a resource to
            be granted to user.
        tot_guaranteed (float): The guaranteed quantity of a
            resource to be granted to the user group in total.
        instance_guaranteed (float): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance.
        user_guaranteed (float): The guaranteed quantity
            of a resource to be granted to user.
    """

    uid = UniqueIdProperty()
    name = StringProperty(required=True)  # TODO choices
    description = StringProperty(default="")
    unit = StringProperty()
    tot_limit = FloatProperty()
    instance_limit = FloatProperty()
    user_limit = FloatProperty()
    tot_guaranteed = FloatProperty(default=0)
    instance_guaranteed = FloatProperty(default=0)
    user_guaranteed = FloatProperty(default=0)

    sla = RelationshipTo(
        ".Service", "APPLIED_RESOURCE_RESTRICTION", cardinality=One
    )
