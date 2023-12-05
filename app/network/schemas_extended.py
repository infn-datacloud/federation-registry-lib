"""Pydantic extended models of the Virtual Machine Network owned by a Provider."""
from typing import Optional

from pydantic import Field

from app.network.schemas import NetworkRead, NetworkReadPublic
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.schemas import NetworkServiceRead, NetworkServiceReadPublic


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Add the provider hosting this region.
    """

    provider: ProviderRead = Field(description="Provider hosting this region")


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Add the provider hosting this region.
    """

    provider: ProviderReadPublic = Field(description="Provider hosting this region")


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB.

    Add the region hosting this service.
    """

    region: RegionReadExtended = Field(description="Provider hosting this service")


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Add the region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(
        description="Provider hosting this service"
    )


class NetworkReadExtended(NetworkRead):
    """Model to extend the Network data read from the DB.

    Add the related project and service.
    """

    project: Optional[ProjectRead] = Field(
        default=None,
        description="List of accessible project. "
        "For private networks at most one item",
    )
    service: NetworkServiceReadExtended = Field(description="Network service")


class NetworkReadExtendedPublic(NetworkReadPublic):
    """Model to extend the Network public data read from the DB.

    Add the related project and service.
    """

    project: Optional[ProjectRead] = Field(
        default=None,
        description="List of accessible project. "
        "For private networks at most one item",
    )
    service: NetworkServiceReadExtendedPublic = Field(description="Network service")
