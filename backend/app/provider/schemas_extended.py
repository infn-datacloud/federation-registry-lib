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
from app.network.schemas import NetworkCreate
from app.project.schemas import ProjectCreate, ProjectRead
from app.provider.schemas import ProviderCreate, ProviderRead, ProviderReadPublic
from app.region.schemas import RegionCreate, RegionRead, RegionReadPublic
from app.service.schemas import (
    BlockStorageServiceCreate,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceCreate,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceCreate,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceCreate,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)
from app.user_group.schemas import UserGroupCreate
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
            IdentityServiceRead,
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
            IdentityServiceReadPublic,
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


class IdentityProviderCreateExtended(IdentityProviderCreate):
    """Model to extend the Identity Provider data used to create a new instance
    in the DB with the authentication method details."""

    relationship: AuthMethodCreate = Field(
        description="Authentication method used by the Provider"
    )
    user_groups: List[UserGroupCreate] = Field(
        default_factory=list,
        description="List of user groups belonging to this identity provider",
    )


class ComputeServiceCreateExtended(ComputeServiceCreate):
    flavors: List[FlavorCreate] = Field(
        default_factory=list,
        description="List of flavors accessible through this service",
    )
    images: List[ImageCreate] = Field(
        default_factory=list,
        description="List of images accessible through this service",
    )


class NetworkServiceCreateExtended(NetworkServiceCreate):
    networks: List[NetworkCreate] = Field(
        default_factory=list,
        description="List of networks accessible through this service",
    )


class RegionCreateExtended(RegionCreate):
    location: Optional[LocationCreate] = Field(
        default=None, description="Geographical site"
    )
    block_storage_services: List[BlockStorageServiceCreate] = Field(
        default_factory=list, description="Block storage service"
    )
    compute_services: List[ComputeServiceCreateExtended] = Field(
        default_factory=list, description="Compute service"
    )
    identity_services: List[IdentityServiceCreate] = Field(
        default_factory=list, description="Identity service"
    )
    network_services: List[NetworkServiceCreateExtended] = Field(
        default_factory=list, description="Network service"
    )


class ProviderCreateExtended(ProviderCreate):
    """Model to extend the Provider data used to create a new instance in the
    DB with the lists of related items."""

    regions: List[RegionCreateExtended] = Field(
        default_factory=list, description="Provider regions."
    )
    identity_providers: List[IdentityProviderCreateExtended] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    projects: List[ProjectCreate] = Field(
        default_factory=list, description="List of owned Projects."
    )
