from typing import List, Optional, Union

from app.location.schemas import LocationRead, LocationReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)
from pydantic import Field


class RegionReadExtended(RegionRead):
    """Model with Region basic attributes."""

    location: Optional[LocationRead] = Field(
        default=None, description="Provider location."
    )
    provider: ProviderRead = Field(description="Provider")
    services: List[
        Union[
            BlockStorageServiceRead,
            ComputeServiceRead,
            IdentityServiceRead,
            NetworkServiceRead,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")


class RegionReadExtendedPublic(RegionReadPublic):
    """Model with Region basic attributes."""

    location: Optional[LocationReadPublic] = Field(
        default=None, description="Provider location."
    )
    provider: ProviderReadPublic = Field(description="Provider")
    services: List[
        Union[
            BlockStorageServiceReadPublic,
            ComputeServiceReadPublic,
            IdentityServiceReadPublic,
            NetworkServiceReadPublic,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")
