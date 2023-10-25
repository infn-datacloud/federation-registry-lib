from typing import List, Optional

from app.network.schemas import NetworkRead, NetworkReadPublic
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.schemas import NetworkServiceRead, NetworkServiceReadPublic
from pydantic import Field


class RegionReadExtended(RegionRead):
    provider: ProviderRead = Field(description="Provider hosting this region")


class RegionReadExtendedPublic(RegionReadPublic):
    provider: ProviderReadPublic = Field(description="Provider hosting this region")


class NetworkServiceReadExtended(NetworkServiceRead):
    region: RegionReadExtended = Field(description="Provider hosting this service")


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    region: RegionReadExtendedPublic = Field(
        description="Provider hosting this service"
    )


class NetworkReadExtended(NetworkRead):
    """Model to extend the Network data read from the DB with the lists of
    related items for authenticated users."""

    project: Optional[ProjectRead] = Field(
        default=None,
        description="List of accessible project. "
        "For private networks at most one item",
    )
    services: List[NetworkServiceReadExtended] = Field(
        default_factory=list, description="Network service"
    )


class NetworkReadExtendedPublic(NetworkReadPublic):
    """Model to extend the Network data read from the DB with the lists of
    related items for non-authenticated users."""

    project: Optional[ProjectRead] = Field(
        default=None,
        description="List of accessible project. "
        "For private networks at most one item",
    )
    services: List[NetworkServiceReadExtendedPublic] = Field(
        default_factory=list, description="Network service"
    )
