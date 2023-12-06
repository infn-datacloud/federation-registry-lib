"""Pydantic extended models of the Region owned by a Provider."""
from typing import List, Optional, Union

from pydantic import Field

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


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Add the provider and location hosting this region and the list of supplied services.
    """

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
    ] = Field(description="List of hosted Services.")


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Add the provider and location hosting this region and the list of supplied services.
    """

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
    ] = Field(description="List of hosted Services.")
