"""Pydantic extended models of the Region owned by a Provider."""

from pydantic import BaseModel, Field

from fedreg.core import BaseNodeRead, BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.location.schemas import LocationRead, LocationReadPublic
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.region.constants import DOC_EXT_LOC, DOC_EXT_PROV, DOC_EXT_SERV
from fedreg.region.schemas import (
    RegionBase,
    RegionBasePublic,
    RegionRead,
    RegionReadPublic,
)
from fedreg.service.schemas import (
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


class RegionReadExtended(BaseNodeRead, BaseReadPrivateExtended, RegionBase):
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
    ] = Field(description=DOC_EXT_SERV)


class RegionReadExtendedPublic(BaseNodeRead, BaseReadPublicExtended, RegionBasePublic):
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
    ] = Field(description=DOC_EXT_SERV)


class RegionReadSingle(BaseModel):
    __root__: (
        RegionReadExtended | RegionRead | RegionReadExtendedPublic | RegionReadPublic
    ) = Field(..., discriminator="schema_type")


class RegionReadMulti(BaseModel):
    __root__: (
        list[RegionReadExtended]
        | list[RegionRead]
        | list[RegionReadExtendedPublic]
        | list[RegionReadPublic]
    ) = Field(..., discriminator="schema_type")
