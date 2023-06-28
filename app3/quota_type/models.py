from neomodel import (
    OneOrMore,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class QuotaType(StructuredNode):
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
    description = StringProperty(default="")
    name = StringProperty(unique_index=True, required=True)
    unit = StringProperty()

    quota = RelationshipFrom(
        "..quota.models.Quota", "HAS_TYPE", cardinality=ZeroOrMore
    )
    service_types = RelationshipFrom(
        "..service_type.models.ServiceType",
        "AVAILABLE_QUOTA_TYPE",
        cardinality=OneOrMore,
    )
