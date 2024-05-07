"""Pydantic extended models of the Region owned by a Provider."""
from typing import List, Optional, Union

from pydantic import Field

from fed_reg.location.schemas import LocationRead, LocationReadPublic
from fed_reg.provider.schemas import ProviderRead, ProviderReadPublic
from fed_reg.region.constants import DOC_EXT_LOC, DOC_EXT_PROV, DOC_EXT_SERV
from fed_reg.region.schemas import RegionRead, RegionReadPublic
from fed_reg.service.schemas import (
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

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderRead): Provider hosting this region.
        location (LocationRead | None): Location hosting this region.
        services (list of Service): Supplied services (block-storage, compute,
            identity and network type).
    """

    location: Optional[LocationRead] = Field(default=None, description=DOC_EXT_LOC)
    provider: ProviderRead = Field(description=DOC_EXT_PROV)
    services: List[
        Union[
            BlockStorageServiceRead,
            ComputeServiceRead,
            IdentityServiceRead,
            NetworkServiceRead,
        ]
    ] = Field(description=DOC_EXT_SERV)


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderReadPublic): Provider hosting this region.
        location (LocationReadPublic | None): Location hosting this region.
        services (list of ServicePublic): Supplied services (block-storage, compute,
            identity and network type).
    """

    location: Optional[LocationReadPublic] = Field(
        default=None, description=DOC_EXT_LOC
    )
    provider: ProviderReadPublic = Field(description=DOC_EXT_PROV)
    services: List[
        Union[
            BlockStorageServiceReadPublic,
            ComputeServiceReadPublic,
            IdentityServiceReadPublic,
            NetworkServiceReadPublic,
        ]
    ] = Field(description=DOC_EXT_SERV)
