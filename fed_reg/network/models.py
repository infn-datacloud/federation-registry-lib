"""Neomodel model of the Virtual Machine Network owned by a Provider."""
from neomodel import (
    ArrayProperty,
    BooleanProperty,
    IntegerProperty,
    One,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrOne,
)


class Network(StructuredNode):
    """Virtual Machine Network owned by a Provider.

    A VM Network is uniquely identified in the Provider by its uuid.
    It has a name and a set of parameters such as the MTU.
    A Network can be public (shared) or private.
    If it is public it has no relationships, otherwise it is connected
    only to the Project who has access.
    When a Project has multiple private or public networks, it is mandatory
    to specify which is the default one.
    For VM using private networks, to access to the VM, users need to use a Proxy.
    To use the Proxy they require the proxy IP and the username to use to access.

    Attributes:
    ----------
        uid (int): Network unique ID.
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        is_shared (bool): Public or private Network.
        is_router_external (bool): Network with access to the outside.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_ip (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): List of tags associated to this Network.
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

    service = RelationshipFrom(
        "fed_reg.service.models.NetworkService",
        "AVAILABLE_NETWORK",
        cardinality=One,
    )
    project = RelationshipFrom(
        "fed_reg.project.models.Project",
        "CAN_USE_NETWORK",
        cardinality=ZeroOrOne,
    )
