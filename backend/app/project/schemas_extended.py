from typing import List, Optional, Union

from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.image.schemas import ImageRead, ImageReadPublic
from app.network.schemas import NetworkRead, NetworkReadPublic
from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
)
from app.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
)
from app.sla.schemas import SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic
from pydantic import Field


class ComputeQuotaReadExtended(ComputeQuotaRead):
    """Model to extend the Quota data read from the DB with the lists of
    related items."""

    service: ComputeServiceRead = Field(
        description="A generic Quota applies to only one generic Service."
    )


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Quota data read from the DB with the lists of
    related items."""

    service: ComputeServiceReadPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    """Model to extend the Quota data read from the DB with the lists of
    related items."""

    service: BlockStorageServiceRead = Field(
        description="A generic Quota applies to only one generic Service."
    )


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Quota data read from the DB with the lists of
    related items."""

    service: BlockStorageServiceReadPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB with the lists of
    related items."""

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group data read from the DB with the lists of
    related items."""

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB with the lists of related
    items."""

    user_group: UserGroupReadExtended = Field(description="Involved User Group.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA data read from the DB with the lists of related
    items."""

    user_group: UserGroupReadExtendedPublic = Field(description="Involved User Group.")


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB with the lists of
    related items for authenticated users."""

    networks: List[NetworkRead] = Field(
        default_factory=list, description="List of accessible networks"
    )
    private_flavors: List[FlavorRead] = Field(
        default_factory=list, description="List of private flavors"
    )
    private_images: List[ImageRead] = Field(
        default_factory=list, description="List of private images"
    )
    provider: ProviderRead = Field(description="Provider owning this Project.")
    quotas: List[
        Union[ComputeQuotaReadExtended, BlockStorageQuotaReadExtended]
    ] = Field(default_factory=list, description="List of owned quotas.")
    sla: Optional[SLAReadExtended] = Field(
        default=None, description="SLA involving this Project."
    )


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project data read from the DB with the lists of
    related items for non-authenticated users."""

    networks: List[NetworkReadPublic] = Field(
        default_factory=list, description="List of accessible networks"
    )
    private_flavors: List[FlavorReadPublic] = Field(
        default_factory=list, description="List of private flavors"
    )
    private_images: List[ImageReadPublic] = Field(
        default_factory=list, description="List of private images"
    )
    provider: ProviderReadPublic = Field(description="Provider owning this Project.")
    quotas: List[
        Union[ComputeQuotaReadExtendedPublic, BlockStorageQuotaReadExtendedPublic]
    ] = Field(default_factory=list, description="List of owned quotas.")
    sla: Optional[SLAReadExtendedPublic] = Field(
        default=None, description="SLA involving this Project."
    )
