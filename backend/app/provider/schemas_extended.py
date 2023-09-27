from typing import List, Optional, Union

from app.auth_method.schemas import AuthMethodCreate, AuthMethodRead
from app.flavor.schemas import FlavorCreate, FlavorRead, FlavorReadPublic
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.image.schemas import ImageCreate, ImageRead, ImageReadPublic
from app.location.schemas import LocationCreate, LocationRead, LocationReadPublic
from app.network.schemas import NetworkCreate, NetworkRead, NetworkReadPublic
from app.project.schemas import ProjectCreate, ProjectRead
from app.provider.schemas import ProviderCreate, ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    BlockStorageQuotaCreate,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaCreate,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
)
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
from app.sla.schemas import SLACreate, SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupCreate, UserGroupRead, UserGroupReadPublic
from pydantic import UUID4, Field


class UserGroupReadExtended(UserGroupRead):
    slas: List[SLARead] = Field(default_factory=list, description="List of SLA")


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    slas: List[SLAReadPublic] = Field(default_factory=list, description="List of SLA")


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB with the
    authentication method details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )
    user_groups: List[UserGroupReadExtended] = Field(
        default_factory=list, description="List of owned users"
    )


class IdentityProviderReadExtendedPublic(IdentityProviderReadPublic):
    """Model to extend the Identity Provider data read from the DB with the
    authentication method details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )
    user_groups: List[UserGroupReadExtendedPublic] = Field(
        default_factory=list, description="List of owned users"
    )


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    quotas: List[BlockStorageQuotaRead] = Field(
        default_factory=list, description="List of quotas"
    )


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    quotas: List[BlockStorageQuotaReadPublic] = Field(
        default_factory=list, description="List of quotas"
    )


class ComputeServiceReadExtended(ComputeServiceRead):
    flavors: List[FlavorRead] = Field(
        default_factory=list, description="List of owned flavors"
    )
    images: List[ImageRead] = Field(
        default_factory=list, description="List of owned images"
    )
    quotas: List[ComputeQuotaRead] = Field(
        default_factory=list, description="List of quotas"
    )


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    flavors: List[FlavorReadPublic] = Field(
        default_factory=list, description="List of owned flavors"
    )
    images: List[ImageReadPublic] = Field(
        default_factory=list, description="List of owned images"
    )
    quotas: List[ComputeQuotaReadPublic] = Field(
        default_factory=list, description="List of quotas"
    )


class NetworkServiceReadExtended(NetworkServiceRead):
    networks: List[NetworkRead] = Field(
        default_factory=list, description="List of owned networks"
    )


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    networks: List[NetworkReadPublic] = Field(
        default_factory=list, description="List of owned networks"
    )


class RegionReadExtended(RegionRead):
    location: Optional[LocationRead] = Field(
        default=None, description="Region geographical location"
    )
    services: List[
        Union[
            BlockStorageServiceReadExtended,
            ComputeServiceReadExtended,
            IdentityServiceRead,
            NetworkServiceReadExtended,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")


class RegionReadExtendedPublic(RegionReadPublic):
    location: Optional[LocationReadPublic] = Field(
        default=None, description="Region geographical location"
    )
    services: List[
        Union[
            BlockStorageServiceReadExtendedPublic,
            ComputeServiceReadExtendedPublic,
            IdentityServiceReadPublic,
            NetworkServiceReadExtendedPublic,
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


class SLACreateExtended(SLACreate):
    projects: List[UUID4] = Field(
        default_factory=list, description="List of projects UUID"
    )


class UserGroupCreateExtended(UserGroupCreate):
    slas: List[SLACreateExtended] = Field(
        default_factory=list, description="List of SLAs"
    )


class IdentityProviderCreateExtended(IdentityProviderCreate):
    """Model to extend the Identity Provider data used to create a new instance
    in the DB with the authentication method details."""

    relationship: AuthMethodCreate = Field(
        description="Authentication method used by the Provider"
    )
    user_groups: List[UserGroupCreateExtended] = Field(
        default_factory=list,
        description="List of user groups belonging to this identity provider",
    )


class BlockStorageQuotaCreateExtended(BlockStorageQuotaCreate):
    project: UUID4 = Field(description="Project UUID")


class ComputeQuotaCreateExtended(ComputeQuotaCreate):
    project: UUID4 = Field(description="Project UUID")


class FlavorCreateExtended(FlavorCreate):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects having access to the private flavor",
    )


class ImageCreateExtended(ImageCreate):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects having access to the private image",
    )


class NetworkCreateExtended(NetworkCreate):
    project: Optional[UUID4] = Field(
        default=None, description="Project having access to a private net"
    )


class BlockStorageServiceCreateExtended(BlockStorageServiceCreate):
    quotas: List[BlockStorageQuotaCreateExtended] = Field(
        default_factory=list, description="List or related quotas"
    )


class ComputeServiceCreateExtended(ComputeServiceCreate):
    flavors: List[FlavorCreateExtended] = Field(
        default_factory=list,
        description="List of flavors accessible through this service",
    )
    images: List[ImageCreateExtended] = Field(
        default_factory=list,
        description="List of images accessible through this service",
    )
    quotas: List[ComputeQuotaCreateExtended] = Field(
        default_factory=list, description="List or related quotas"
    )


class NetworkServiceCreateExtended(NetworkServiceCreate):
    networks: List[NetworkCreateExtended] = Field(
        default_factory=list,
        description="List of networks accessible through this service",
    )


class RegionCreateExtended(RegionCreate):
    location: Optional[LocationCreate] = Field(
        default=None, description="Geographical site"
    )
    block_storage_services: List[BlockStorageServiceCreateExtended] = Field(
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
