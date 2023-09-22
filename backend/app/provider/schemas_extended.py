from typing import List, Optional, Union

from app.auth_method.schemas import AuthMethodCreate, AuthMethodRead
from app.flavor.schemas import FlavorCreate
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.image.schemas import ImageCreate
from app.location.schemas import LocationCreate, LocationRead, LocationReadPublic
from app.project.schemas import ProjectCreate, ProjectRead
from app.provider.schemas import ProviderCreate, ProviderRead, ProviderReadPublic
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.schemas import (
    BlockStorageServiceCreate,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceCreate,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    KeystoneServiceCreate,
    KeystoneServiceRead,
    KeystoneServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)
from pydantic import Field


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB with the
    authentication method details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class IdentityProviderReadExtendedPublic(IdentityProviderReadPublic):
    """Model to extend the Identity Provider data read from the DB with the
    authentication method details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class RegionReadExtended(RegionRead):
    location: Optional[LocationRead] = Field(
        default=None, description="Region geographical location"
    )
    services: List[
        Union[
            BlockStorageServiceRead,
            ComputeServiceRead,
            KeystoneServiceRead,
            NetworkServiceRead,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")


class RegionReadExtendedPublic(RegionReadPublic):
    location: Optional[LocationReadPublic] = Field(
        default=None, description="Region geographical location"
    )
    services: List[
        Union[
            BlockStorageServiceReadPublic,
            ComputeServiceReadPublic,
            KeystoneServiceReadPublic,
            NetworkServiceReadPublic,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")


class ProviderReadExtended(ProviderRead):
    """Model to extend the Provider data read from the DB with the lists of
    related items for authenticated users."""

    identity_providers: List[IdentityProviderReadExtended] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    projects: List[ProjectRead] = Field(
        default_factory=list, description="List of owned Projects."
    )
    regions: List[RegionReadExtended] = Field(
        default_factory=list, description="List of available regions"
    )


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Provider data read from the DB with the lists of
    related items for non-authenticated users."""

    identity_providers: List[IdentityProviderReadExtendedPublic] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    projects: List[ProjectRead] = Field(
        default_factory=list, description="List of owned Projects."
    )
    regions: List[RegionReadExtendedPublic] = Field(
        default_factory=list, description="List of available regions"
    )


###############################################
class IdentityProviderCreateExtended(IdentityProviderCreate):
    """Model to extend the Identity Provider data used to create a new instance
    in the DB with the authentication method details."""

    relationship: AuthMethodCreate = Field(
        description="Authentication method used by the Provider"
    )


class ProviderCreateExtended(ProviderCreate):
    """Model to extend the Provider data used to create a new instance in the
    DB with the lists of related items."""

    location: Optional[LocationCreate] = Field(
        default=None, description="Provider location."
    )
    flavors: List[FlavorCreate] = Field(
        default_factory=list, description="List of owned Flavors."
    )
    identity_providers: List[IdentityProviderCreateExtended] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    images: List[ImageCreate] = Field(
        default_factory=list, description="List of owned Images."
    )
    projects: List[ProjectCreate] = Field(
        default_factory=list, description="List of owned Projects."
    )
    services: List[
        Union[BlockStorageServiceCreate, KeystoneServiceCreate, ComputeServiceCreate]
    ] = Field(default_factory=list, description="List of hosted Services.")
