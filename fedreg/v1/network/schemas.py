"""Pydantic models of the Virtual Machine Network owned by a Provider."""

from typing import Literal

from pydantic import Field

from fedreg.v1.core import (
    BaseNode,
    BaseNodeCreate,
    BaseNodeRead,
    BaseReadPrivate,
    BaseReadPublic,
    create_query_model,
)
from fedreg.v1.network.constants import (
    DOC_DEFAULT,
    DOC_MTU,
    DOC_NAME,
    DOC_OUT_ROUTER,
    DOC_PROXY_HOST,
    DOC_PROXY_USER,
    DOC_SHARED,
    DOC_TAGS,
    DOC_UUID,
)


class NetworkBasePublic(BaseNode):
    """Model with Network public attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
    """

    name: str = Field(description=DOC_NAME)
    uuid: str = Field(description=DOC_UUID)


class NetworkBase(NetworkBasePublic):
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

    is_router_external: bool = Field(default=False, description=DOC_OUT_ROUTER)
    is_default: bool = Field(default=False, description=DOC_DEFAULT)
    mtu: int | None = Field(default=None, gt=0, description=DOC_MTU)
    proxy_host: str | None = Field(default=None, description=DOC_PROXY_HOST)
    proxy_user: str | None = Field(default=None, description=DOC_PROXY_USER)
    tags: list[str] = Field(default_factory=list, description=DOC_TAGS)


class PrivateNetworkCreate(BaseNodeCreate, NetworkBase):
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

    is_shared: Literal[False] = Field(default=False, description=DOC_SHARED)


class SharedNetworkCreate(BaseNodeCreate, NetworkBase):
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

    is_shared: Literal[True] = Field(default=True, description=DOC_SHARED)


class NetworkUpdate(BaseNodeCreate, NetworkBase):
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

    name: str | None = Field(default=None, description=DOC_NAME)
    uuid: str | None = Field(default=None, description=DOC_UUID)


class NetworkReadPublic(BaseNodeRead, BaseReadPublic, NetworkBasePublic):
    """Model, for non-authenticated users, to read Network data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Network unique ID.
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
    """


class NetworkRead(BaseNodeRead, BaseReadPrivate, NetworkBase):
    """Model, for authenticated users, to read Network data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Network unique ID.
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

    is_shared: bool | None = Field(default=None, description=DOC_SHARED)


NetworkQuery = create_query_model("NetworkQuery", NetworkBase)
