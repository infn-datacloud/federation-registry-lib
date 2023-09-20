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
from app.project.schemas import ProjectCreate, ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderCreate, ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
)
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
)
from app.sla.schemas import SLARead, SLAReadPublic
from pydantic import Field


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB."""

    quotas: List[Union[ComputeQuotaRead, BlockStorageQuotaRead]] = Field(
        default_factory=list, description="List of owned quotas."
    )
    sla: Optional[SLARead] = Field(
        default=None, description="SLA involving this Project."
    )


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project data read from the DB."""

    quotas: List[Union[ComputeQuotaReadPublic, BlockStorageQuotaReadPublic]] = Field(
        default_factory=list, description="List of owned quotas."
    )
    sla: Optional[SLAReadPublic] = Field(
        default=None, description="SLA involving this Project."
    )


class IdentityProviderCreateExtended(IdentityProviderCreate):
    """Model to extend the Identity Provider data used to create a new instance
    in the DB with the authentication method details."""

    relationship: AuthMethodCreate = Field(
        description="Authentication method used by the Provider"
    )


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


class ProviderReadExtended(ProviderRead):
    """Model to extend the Provider data read from the DB with the lists of
    related items for authenticated users."""

    location: Optional[LocationRead] = Field(
        default=None, description="Provider location."
    )
    flavors: List[FlavorRead] = Field(
        default_factory=list, description="List of owned Flavors."
    )
    identity_providers: List[IdentityProviderReadExtended] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    images: List[ImageRead] = Field(
        default_factory=list, description="List of owned Images."
    )
    projects: List[ProjectReadExtended] = Field(
        default_factory=list, description="List of owned Projects."
    )
    services: List[
        Union[BlockStorageServiceRead, KeystoneServiceRead, ComputeServiceRead]
    ] = Field(default_factory=list, description="List of hosted Services.")


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Provider data read from the DB with the lists of
    related items for non-authenticated users."""

    location: Optional[LocationReadPublic] = Field(
        default=None, description="Provider location."
    )
    flavors: List[FlavorReadPublic] = Field(
        default_factory=list, description="List of owned Flavors."
    )
    identity_providers: List[IdentityProviderReadExtendedPublic] = Field(
        default_factory=list,
        description="List of supported identity providers.",
    )
    images: List[ImageReadPublic] = Field(
        default_factory=list, description="List of owned Images."
    )
    projects: List[ProjectReadExtendedPublic] = Field(
        default_factory=list, description="List of owned Projects."
    )
    services: List[
        Union[
            BlockStorageServiceReadPublic,
            KeystoneServiceReadPublic,
            ComputeServiceReadPublic,
        ]
    ] = Field(default_factory=list, description="List of hosted Services.")
