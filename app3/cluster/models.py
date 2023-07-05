from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    RelationshipFrom,
    OneOrMore,
)


class Cluster(StructuredNode):
    """Virtual Machine Cluster class.

    A VM/Docker Cluster has a number of CPUs and GPUs.
    It has a fixed RAM and disk size. It can be supported
    by multiple providers and can be accessible to a
    subset of user groups.

    Attributes:
        uid (int): Cluster unique ID.
        description (str): Brief description.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): TODO
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")

    providers = RelationshipFrom(
        "..provider.models.Provider",
        "AVAILABLE_CLUSTER",
        cardinality=OneOrMore,
    )
