from typing import Any, List, Optional, Union

from pydantic import Field

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
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
)
from app.sla.schemas import SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Service data read from the DB with the parent region."""

    region: RegionRead = Field(description="Region hosting this service.")


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Service data read from the DB with the parent region."""

    region: RegionReadPublic = Field(description="Region hosting this service.")


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    """Model to extend the Service data read from the DB with the parent region."""

    region: RegionRead = Field(description="Region hosting this service.")


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the Service data read from the DB with the parent region."""

    region: RegionReadPublic = Field(description="Region hosting this service.")


class ComputeQuotaReadExtended(ComputeQuotaRead):
    """Model to extend the Quota data read from the DB with the lists of related
    items.
    """

    service: ComputeServiceReadExtended = Field(
        description="A generic Quota applies to only one generic Service."
    )


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Quota data read from the DB with the lists of related
    items.
    """

    service: ComputeServiceReadExtendedPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    """Model to extend the Quota data read from the DB with the lists of related
    items.
    """

    service: BlockStorageServiceReadExtended = Field(
        description="A generic Quota applies to only one generic Service."
    )


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Quota data read from the DB with the lists of related
    items.
    """

    service: BlockStorageServiceReadExtendedPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB with the lists of related
    items.
    """

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group data read from the DB with the lists of related
    items.
    """

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB with the lists of related items."""

    user_group: UserGroupReadExtended = Field(description="Involved User Group.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA data read from the DB with the lists of related items."""

    user_group: UserGroupReadExtendedPublic = Field(description="Involved User Group.")


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB with the lists of related items
    for authenticated users.
    """

    flavors: List[FlavorRead] = Field(
        default_factory=list, description="List of flavors"
    )
    images: List[ImageRead] = Field(default_factory=list, description="List of images")
    networks: List[NetworkRead] = Field(
        default_factory=list, description="List of networks"
    )
    provider: ProviderRead = Field(description="Provider owning this Project.")
    quotas: List[
        Union[ComputeQuotaReadExtended, BlockStorageQuotaReadExtended]
    ] = Field(default_factory=list, description="List of owned quotas.")
    sla: Optional[SLAReadExtended] = Field(
        default=None, description="SLA involving this Project."
    )

    @classmethod
    def from_orm(cls, obj: Any) -> "ProjectReadExtended":
        # `obj` is the orm model instance
        obj.flavors = obj.public_flavors() + obj.private_flavors.all()
        obj.images = obj.public_images() + obj.private_images.all()
        obj.networks = obj.public_networks() + obj.private_networks.all()
        return super().from_orm(obj)


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project data read from the DB with the lists of related items
    for non-authenticated users.
    """

    networks: List[NetworkReadPublic] = Field(
        default_factory=list, description="List of networks"
    )
    flavors: List[FlavorReadPublic] = Field(
        default_factory=list, description="List of flavors"
    )
    images: List[ImageReadPublic] = Field(
        default_factory=list, description="List of images"
    )
    provider: ProviderReadPublic = Field(description="Provider owning this Project.")
    quotas: List[
        Union[ComputeQuotaReadExtendedPublic, BlockStorageQuotaReadExtendedPublic]
    ] = Field(default_factory=list, description="List of owned quotas.")
    sla: Optional[SLAReadExtendedPublic] = Field(
        default=None, description="SLA involving this Project."
    )

    @classmethod
    def from_orm(cls, obj: Any) -> "ProjectReadExtended":
        # `obj` is the orm model instance
        obj.flavors = obj.public_flavors() + obj.private_flavors.all()
        obj.images = obj.public_images() + obj.private_images.all()
        obj.networks = obj.public_networks() + obj.private_networks.all()
        return super().from_orm(obj)
