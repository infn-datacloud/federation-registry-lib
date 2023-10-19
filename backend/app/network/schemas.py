from typing import List, Optional
from uuid import UUID

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import Field, validator


class NetworkBase(BaseNode):
    """Model with Network basic attributes."""

    name: str = Field(description="Network name in the provider.")
    uuid: str = Field(description="Network UUID in the provider.")
    is_shared: bool = Field(
        default=True,
        description="Public (accessible to all projects) or private network type",
    )
    is_router_external: bool = Field(default=False, description="External network")
    is_default: bool = Field(
        default=False, description="Main network to use when creating a VM or docker"
    )
    mtu: Optional[int] = Field(default=None, description="Metric transmission unit")
    proxy_ip: Optional[str] = Field(
        default=None,
        description="Proxy IP address to use to access to private networks",
    )
    proxy_user: Optional[str] = Field(
        default=None, description="Proxy username to use to access to private networks"
    )
    tags: List[str] = Field(default_factory=list, description="List of network tags")

    @validator("uuid", pre=True)
    def to_string(cls, v):
        if isinstance(v, UUID):
            return v.hex
        return v


class NetworkCreate(BaseNodeCreate, NetworkBase):
    """Model to create a Network.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class NetworkUpdate(BaseNodeCreate, NetworkBase):
    """Model to update a Network.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    name: Optional[str] = Field(
        default=None, description="Network name in the provider."
    )
    uuid: Optional[str] = Field(
        default=None, description="Network UUID in the provider."
    )


class NetworkRead(BaseNodeRead, NetworkBase):
    """Model to read Network data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class NetworkReadPublic(BaseNodeRead, NetworkBase):
    pass


class NetworkReadShort(BaseNodeRead, NetworkBase):
    pass


NetworkQuery = create_query_model("NetworkQuery", NetworkBase)
