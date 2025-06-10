"""Pydantic extended models of the Region owned by a Provider."""

from pydantic.v1 import Field

from fedreg.v1.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.v1.location.schemas import LocationRead, LocationReadPublic
from fedreg.v1.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.v1.region.constants import DOC_EXT_LOC, DOC_EXT_PROV, DOC_EXT_SERV
from fedreg.v1.region.schemas import RegionRead, RegionReadPublic
from fedreg.v1.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    ObjectStoreServiceRead,
    ObjectStoreServiceReadPublic,
)


class RegionReadExtended(BaseReadPrivateExtended, RegionRead):
    """Model to extend the Region data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        overbooking_cpu (float): CPU overbooking factor.
        overbooking_ram (float): RAM overbooking factor.
        bandwidth_in (float): Bandwidth in.
        bandwidth_out (float): Bandwidth out.
        provider (ProviderRead): Provider hosting this region.
        location (LocationRead | None): Location hosting this region.
        services (list of Service): Supplied services (block-storage, compute,
            identity and network type).
    """

    location: LocationRead | None = Field(default=None, description=DOC_EXT_LOC)
    provider: ProviderRead = Field(description=DOC_EXT_PROV)
    services: list[
        BlockStorageServiceRead
        | ComputeServiceRead
        | IdentityServiceRead
        | NetworkServiceRead
        | ObjectStoreServiceRead
    ] = Field(default_factory=list, description=DOC_EXT_SERV)


class RegionReadExtendedPublic(BaseReadPublicExtended, RegionReadPublic):
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

    location: LocationReadPublic | None = Field(default=None, description=DOC_EXT_LOC)
    provider: ProviderReadPublic = Field(description=DOC_EXT_PROV)
    services: list[
        BlockStorageServiceReadPublic
        | ComputeServiceReadPublic
        | IdentityServiceReadPublic
        | NetworkServiceReadPublic
        | ObjectStoreServiceReadPublic
    ] = Field(default_factory=list, description=DOC_EXT_SERV)
