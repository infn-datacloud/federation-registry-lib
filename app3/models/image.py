from neomodel import (
    BooleanProperty,
    DateTimeProperty,
    OneOrMore,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    ZeroOrMore,
)


class SupportedImage(StructuredRel):
    """Supported Image class.

    Relationship linking a image to the provider supporting it.

    Attributes:
        uid (uuid): SupportedImage unique ID.
        image_name (str): Name given to the Image by the Provider.
        image_id (uuid): Image Unique ID in the Provider.
    """

    uid = UniqueIdProperty()
    image_name = StringProperty(required=True)
    image_id = StringProperty(required=True)


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
    os = StringProperty(required=True)  # TODO: add choices
    distribution = StringProperty(required=True)
    version = StringProperty(required=True)
    architecture = StringProperty(required=True)
    cuda_support: BooleanProperty(default=False)
    gpu_driver: BooleanProperty(default=False)
    creation_time: DateTimeProperty()

    provider = RelationshipFrom(
        ".Provider",
        "SUPPORTED_VM_IMAGE",
        cardinality=OneOrMore,
        model=SupportedImage,
    )
    user_group = RelationshipFrom(
        ".UserGroup", "AVAILABLE_VM_IMAGE", cardinality=ZeroOrMore
    )
