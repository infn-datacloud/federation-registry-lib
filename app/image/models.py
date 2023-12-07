"""Neomodel model of the Virtual Machine Image owned by a Provider."""
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
    """Virtual Machine Image owned by a Provider.

    A VM Image is uniquely identified in the Provider by its uuid.
    It has a name and a set of parameters such as OS type, OS distribution,
    OS version and architecture. It can support cuda and gpus.
    An Image can be public or private.
    If it is public it has no relationships, otherwise it is connected to
    all and only the Projects who have access.

    Attributes:
    ----------
        uid (int): Image unique ID.
        description (str): Brief description.
        name (str): Image name in the Provider.
        uuid (str): Image unique ID in the Provider
        os_type (str | None): OS type.
        os_distro (str | None): OS distribution.
        os_version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        kernel_id (str | None): Kernel version.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs drivers.
        is_public (bool): Public or private Image.
        tags (list of str): List of tags associated to this Image.
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
    # TODO Understand what does it mean and add to documentation
    cuda_support = BooleanProperty(default=False)
    # TODO Understand what does it mean and add to documentation
    gpu_driver = BooleanProperty(default=False)
    is_public = BooleanProperty(default=True)
    tags = ArrayProperty(StringProperty())

    services = RelationshipFrom(
        "app.service.models.ComputeService",
        "AVAILABLE_VM_IMAGE",
        cardinality=OneOrMore,
    )
    projects = RelationshipFrom(
        "app.project.models.Project",
        "CAN_USE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
