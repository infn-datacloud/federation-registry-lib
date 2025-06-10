"""Pydantic models of the Virtual Machine Network owned by a Provider."""

from typing import Annotated, Literal

from pydantic import Field

from fedreg.v2.core import BaseNode, BaseNodeRead, PaginationQuery


class NetworkBase(BaseNode):
    """Model with Network public and restricted attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        is_router_external (bool): Network with access to outside networks. External
            network.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_host (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): list of tags associated to this Network.
    """

    name: Annotated[str, Field(description="Network name in the Resource Provider.")]
    uuid: Annotated[
        str, Field(description="Network unique ID in the Resource Provider.")
    ]
    mtu: Annotated[
        int | None,
        Field(default=None, gt=0, description="Metric transmission unit (B)."),
    ]
    tags: Annotated[
        list[str],
        Field(
            default_factory=list, description="List of tags associated to this Network."
        ),
    ]
    is_default: Annotated[
        bool, Field(default=False, description="Network to use as default.")
    ]


class PrivateNetworkCreate(NetworkBase):
    """Model to create a Network.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        is_router_external (bool): Network with access to outside networks. External
            network.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_host (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): list of tags associated to this Network.
        is_shared (bool): Public or private Network.
    """

    is_router_external: Annotated[
        Literal[False],
        Field(
            default=False,
            description="Network with access to outside networks. External/public net.",
        ),
    ]
    proxy_host: Annotated[
        str | None,
        Field(
            default=None,
            description="Proxy IP address or hostname. Accept port number.",
        ),
    ]
    proxy_user: Annotated[
        str | None, Field(default=None, description="Proxy username.")
    ]


class PublicNetworkCreate(NetworkBase):
    """Model to create a Network.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        is_router_external (bool): Network with access to outside networks. External
            network.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_host (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): list of tags associated to this Network.
        is_shared (bool): Public or private Network.
    """

    is_router_external: Annotated[
        Literal[True],
        Field(
            default=True,
            description="Network with access to outside networks. External/public net.",
        ),
    ]


class NetworkRead(BaseNodeRead, NetworkBase):
    """Model, for authenticated users, to read Network data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *id* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        id (int): Network unique ID.
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        is_router_external (bool): Network with access to outside networks. External
            network.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_host (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): list of tags associated to this Network.
        is_shared (bool): Public or private Network.
    """

    is_router_external: Annotated[
        bool,
        Field(
            default=False,
            description="Network with access to outside networks. External/public net.",
        ),
    ]
    proxy_host: Annotated[
        str | None,
        Field(
            default=None,
            description="Proxy IP address or hostname. Accept port number.",
        ),
    ]
    proxy_user: Annotated[
        str | None, Field(default=None, description="Proxy username.")
    ]


class NetworkQuery(PaginationQuery):
    """Model to update a Network.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): Network name in the Provider.
        uuid (str | None): Network unique ID in the Provider
        is_router_external (bool | None): Network with access to outside networks.
            External network.
        is_default (bool | None): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_host (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str | None): list of tags associated to this Network.
    """

    name: Annotated[
        str | None,
        Field(default=None, description="Network name in the Resource Provider."),
    ]
    uuid: Annotated[
        str | None,
        Field(default=None, description="Network unique ID in the Resource Provider."),
    ]
    mtu: Annotated[
        int | None,
        Field(default=None, gt=0, description="Metric transmission unit (B)."),
    ]
    tags: Annotated[
        list[str] | None,
        Field(default=None, description="List of tags associated to this Network."),
    ]
    is_router_external: Annotated[
        bool | None,
        Field(
            default=None,
            description="Network with access to outside networks. External/public net.",
        ),
    ]
    proxy_host: Annotated[
        str | None,
        Field(
            default=None,
            description="Proxy IP address or hostname. Accept port number.",
        ),
    ]
    proxy_user: Annotated[
        str | None, Field(default=None, description="Proxy username.")
    ]
    is_default: Annotated[
        bool | None, Field(default=None, description="Network to use as default.")
    ]
