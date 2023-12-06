"""Pydantic models of the Virtual Machine Network owned by a Provider."""
from typing import List, Optional

from pydantic import Field

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class NetworkBasePublic(BaseNode):
    """Model with Network public attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
    """

    name: str = Field(description="Network name in the provider.")
    uuid: str = Field(description="Network UUID in the provider.")


class NetworkBase(NetworkBasePublic):
    """Model with Network public and restricted attributes.

    Attributes:
    ----------
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

    is_shared: bool = Field(
        default=True,
        description="Public (accessible to all projects) or private network type",
    )
    is_router_external: bool = Field(default=False, description="External network")
    is_default: bool = Field(
        default=False,
        description="Main network to use when creating a VM or docker",
    )
    mtu: Optional[int] = Field(default=None, description="Metric transmission unit")
    proxy_ip: Optional[str] = Field(
        default=None,
        description="Proxy IP address to use to access to private networks",
    )
    proxy_user: Optional[str] = Field(
        default=None,
        description="Proxy username to use to access to private networks",
    )
    tags: List[str] = Field(default_factory=list, description="List of network tags")


class NetworkCreate(BaseNodeCreate, NetworkBase):
    """Model to create a Network.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
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
        is_shared (bool | None): Public or private Network.
        is_router_external (bool | None): Network with access to the outside.
        is_default (bool | None): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_ip (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str | None): List of tags associated to this Network.
    """

    name: Optional[str] = Field(
        default=None, description="Network name in the provider."
    )
    uuid: Optional[str] = Field(
        default=None, description="Network UUID in the provider."
    )


class NetworkReadPublic(BaseNodeRead, NetworkBasePublic):
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


class NetworkRead(BaseNodeRead, NetworkBase):
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
        is_shared (bool): Public or private Network.
        is_router_external (bool): Network with access to the outside.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_ip (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): List of tags associated to this Network.
    """


NetworkQuery = create_query_model("NetworkQuery", NetworkBase)
