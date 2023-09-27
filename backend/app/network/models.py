from neomodel import (
    ArrayProperty,
    BooleanProperty,
    IntegerProperty,
    OneOrMore,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrOne,
)


class Network(StructuredNode):
    """Virtual Machine Network class.

    A VM/Docker Network has a number of CPUs and GPUs.
    It has a fixed RAM and disk size. It can be supported
    by multiple providers and can be accessible to a
    subset of user groups.

    Attributes:
        uid (int): Network unique ID.
        description (str): Brief description.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
    is_shared = BooleanProperty(default=False)
    is_router_external = BooleanProperty(default=False)
    is_default = BooleanProperty(default=False)
    mtu = IntegerProperty()
    proxy_ip = StringProperty()
    proxy_user = StringProperty()
    tags = ArrayProperty(StringProperty())

    services = RelationshipFrom(
        "..service.models.NetworkService",
        "AVAILABLE_NETWORK",
        cardinality=OneOrMore,
    )
    project = RelationshipFrom(
        "..project.models.Project",
        "CAN_USE_NETWORK",
        cardinality=ZeroOrOne,
    )
