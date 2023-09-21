from neomodel import (
    BooleanProperty,
    One,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
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
    public = BooleanProperty(default=False)
    external = BooleanProperty(default=False)
    preferred = BooleanProperty(default=False)
    proxy_ip = StringProperty()
    proxy_user = StringProperty()

    service = RelationshipFrom(
        "..service.models.NetworkService",
        "AVAILABLE_NETWORK",
        cardinality=One,
    )
    projects = RelationshipFrom(
        "..project.models.Project",
        "CAN_USE_NETWORK",
        cardinality=ZeroOrMore,
    )
