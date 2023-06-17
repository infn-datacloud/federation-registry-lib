from neomodel import (
    FloatProperty,
    StringProperty,
    StructuredRel,
    UniqueIdProperty,
)


class Quota(StructuredRel):
    """Associated Project class.

    Relationship linking a user group to a provider.
    This link correspond to a "project/tenant" entity.

    Attributes:
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
    type = StringProperty(required=True)
    unit = StringProperty()
    tot_limit = FloatProperty()
    tot_guaranteed = FloatProperty(default=0)
    user_limit = FloatProperty()
    user_guaranteed = FloatProperty(default=0)
    instance_limit = FloatProperty()
    instance_guaranteed = FloatProperty(default=0)
