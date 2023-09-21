from typing import Optional

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import UUID4, Field


class NetworkBase(BaseNode):
    """Model with Network basic attributes."""

    name: str = Field(description="Network name in the provider.")
    uuid: UUID4 = Field(description="Network UUID in the provider.")
    public: bool = Field(default=False, description="Public or private network type")
    external: bool = Field(default=False, description="External network")
    preferred: bool = Field(
        default=False, description="Main network to use when creating a VM or docker"
    )
    proxy_ip: Optional[str] = Field(
        default=None,
        description="Proxy IP address to use to access to private networks",
    )
    proxy_user: Optional[str] = Field(
        default=None, description="Proxy username to use to access to private networks"
    )


class NetworkCreate(BaseNodeCreate, NetworkBase):
    """Model to create a Network.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class NetworkUpdate(NetworkCreate):
    """Model to update a Network.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    name: Optional[str] = Field(
        default=None, description="Network name in the provider."
    )
    uuid: Optional[UUID4] = Field(
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
