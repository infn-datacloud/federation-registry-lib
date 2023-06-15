from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    BooleanProperty,
    UniqueIdProperty,
    RelationshipFrom,
    OneOrMore,
)
from ..relationships import AvailableVMFlavor


class Flavor(StructuredNode):
    """Virtual Machine Flavor class.

    A VM/Docker Flavor has a number of CPUs and GPUs.
    It has a fixed RAM and disk size. It can be supported
    by multiple providers and can be accessible to a
    subset of user groups.

    Attributes:
        uid (int): Flavor unique ID.
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
    num_vcpus = IntegerProperty(default=0)
    num_gpus = IntegerProperty(default=0)
    ram = IntegerProperty(default=0)
    disk = IntegerProperty(default=0)
    infiniband_support = BooleanProperty(default=False)
    gpu_model = StringProperty()
    gpu_vendor = StringProperty()

    providers = RelationshipFrom(
        ".Provider",
        "AVAILABLE_VM_FLAVOR",
        cardinality=OneOrMore,
        model=AvailableVMFlavor,
    )
