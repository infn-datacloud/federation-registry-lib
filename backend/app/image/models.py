from neomodel import (
    ArrayProperty,
    BooleanProperty,
    OneOrMore,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class Image(StructuredNode):
    """Virtual Machine Image class.

    A VM/Docker Image is defined by: OS, distribution,
    version and architecture. It can support cuda or gpus.
    It has a creation time. It can be supported by multiple
    providers and can be accessible to a subset of user
    groups.

    Attributes:
        uid (int): Image unique ID.
        description (str): Brief description.
        os (str): Image Operating System.
        distribution (str): OS distribution.
        version (str): Distribution version.
        architecture (str): OS architecture.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs.
        creation_time (datetime): Image creation time.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
    os_type = StringProperty()
    os_distro = StringProperty()
    os_version = StringProperty()
    architecture = StringProperty()
    kernel_id = StringProperty()
    # TODO Understand what does it mean
    cuda_support = BooleanProperty(default=False)
    # TODO Understand what does it mean
    gpu_driver = BooleanProperty(default=False)
    is_public = BooleanProperty(default=True)
    tags = ArrayProperty(StringProperty())

    services = RelationshipFrom(
        "..service.models.ComputeService",
        "AVAILABLE_VM_IMAGE",
        cardinality=OneOrMore,
    )
    projects = RelationshipFrom(
        "..project.models.Project",
        "CAN_USE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
