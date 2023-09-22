from typing import List

from app.network.schemas import NetworkRead, NetworkReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
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

    projects: List[ProjectRead] = Field(
        default_factory=list,
        description="List of accessible project. "
        "For private networks at most one item",
    )
    service: NetworkServiceReadExtended = Field(description="Network service")


class NetworkReadExtendedPublic(NetworkReadPublic):
    """Model to extend the Network data read from the DB with the lists of
    related items for non-authenticated users."""

    projects: List[ProjectReadPublic] = Field(
        default_factory=list,
        description="List of accessible project. "
        "For private networks at most one item",
    )
    service: NetworkServiceReadExtendedPublic = Field(description="Network service")
