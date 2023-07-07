from neomodel import (
    FloatProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class Quota(StructuredNode):
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

    project = RelationshipFrom(
        "..project.models.Project", "USE_SERVICE_WITH_QUOTA", cardinality=One
    )
    service = RelationshipTo(
        "..service.models.Service", "APPLIES_TO", cardinality=One
    )


class UploadBandwidthQuota(Quota):
    pass


class DownloadBandwidthQuota(Quota):
    pass


class NumCPUQuota(Quota):
    pass


class PublicIPQuota(Quota):
    pass


class CPUFrequencyQuota(Quota):
    pass


class MoneyQuota(Quota):
    pass


class RAMQuota(Quota):
    pass


class DiskQuota(Quota):
    pass


class UploadAggregatedQuota(Quota):
    pass


class DownloadAggregatedQuota(Quota):
    pass


class ComputeTimeQuota(Quota):
    pass
