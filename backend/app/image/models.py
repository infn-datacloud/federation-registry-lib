from neomodel import (
    BooleanProperty,
    DateTimeProperty,
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
    os = StringProperty()
    distribution = StringProperty()
    version = StringProperty()
    architecture = StringProperty()
    cuda_support = BooleanProperty(default=False)
    gpu_driver = BooleanProperty(default=False)
    creation_time = DateTimeProperty()
    is_public = BooleanProperty(default=True)

    service = RelationshipFrom(
        "..service.models.ComputeService",
        "AVAILABLE_VM_IMAGE",
        cardinality=OneOrMore,
    )
    projects = RelationshipFrom(
        "..project.models.Project",
        "CAN_USE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
