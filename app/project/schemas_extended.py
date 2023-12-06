"""Pydantic extended models of the Project owned by a Provider."""
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
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
)
from app.region.schemas import RegionRead, RegionReadPublic
from app.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)
from app.sla.schemas import SLARead, SLAReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    """Model to extend the Block Storage Service data read from the DB.

    Add the region hosting it.
    """

    region: RegionRead = Field(description="Region hosting this service.")


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the Block Storage Service public data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadPublic = Field(description="Region hosting this service.")


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB.

    Add the region hosting it.
    """

    region: RegionRead = Field(description="Region hosting this service.")


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadPublic = Field(description="Region hosting this service.")


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB.

    Add the region hosting it.
    """

    region: RegionRead = Field(description="Region hosting this service.")


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadPublic = Field(description="Region hosting this service.")


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    """Model to extend the Block Storage Quota data read from the DB.

    Add the target block storage service.
    """

    service: BlockStorageServiceReadExtended = Field(
        description="A generic Quota applies to only one generic Service."
    )


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Block Storage Quota public data read from the DB.

    Add the target block storage service.
    """

    service: BlockStorageServiceReadExtendedPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class ComputeQuotaReadExtended(ComputeQuotaRead):
    """Model to extend the Compute Quota data read from the DB.

    Add the target compute service.
    """

    service: ComputeServiceReadExtended = Field(
        description="A generic Quota applies to only one generic Service."
    )


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Compute Quota public data read from the DB.

    Add the target compute service.
    """

    service: ComputeServiceReadExtendedPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class NetworkQuotaReadExtended(NetworkQuotaRead):
    """Model to extend the Network Quota data read from the DB.

    Add the target network service.
    """

    service: NetworkServiceReadExtended = Field(
        description="A generic Quota applies to only one generic Service."
    )


class NetworkQuotaReadExtendedPublic(NetworkQuotaReadPublic):
    """Model to extend the Network Quota public data read from the DB.

    Add the target network service.
    """

    service: NetworkServiceReadExtendedPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB.

    Add the identity provider owning this user group.
    """

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group public data read from the DB.

    Add the identity provider owning this user group.
    """

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB.

    Add the user group involved in this SLA.
    """

    user_group: UserGroupReadExtended = Field(description="Involved User Group.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA public data read from the DB.

    Add the user group involved in this SLA.
    """

    user_group: UserGroupReadExtendedPublic = Field(description="Involved User Group.")


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB.

    Add the list of networks, flavors and images (publics and privates), the list of
    quotas (any type), the SLA targeting this project and the provider hosting it.
    """

    flavors: List[FlavorRead] = Field(description="List of flavors")
    images: List[ImageRead] = Field(description="List of images")
    networks: List[NetworkRead] = Field(description="List of networks")
    provider: ProviderRead = Field(description="Provider owning this Project.")
    quotas: List[
        Union[
            ComputeQuotaReadExtended,
            BlockStorageQuotaReadExtended,
            NetworkQuotaReadExtended,
        ]
    ] = Field(description="List of owned quotas.")
    sla: Optional[SLAReadExtended] = Field(
        default=None, description="SLA involving this Project."
    )

    @classmethod
    def from_orm(cls, obj: Any) -> "ProjectReadExtended":
        """Method to merge public and private flavors, images and networks.

        `obj` is the orm model instance.
        """
        obj.flavors = obj.public_flavors() + obj.private_flavors.all()
        obj.images = obj.public_images() + obj.private_images.all()
        obj.networks = obj.public_networks() + obj.private_networks.all()
        return super().from_orm(obj)


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project public data read from the DB.

    Add the list of networks, flavors and images (publics and privates), the list of
    quotas (any type), the SLA targeting this project and the provider hosting it.
    """

    networks: List[NetworkReadPublic] = Field(description="List of networks")
    flavors: List[FlavorReadPublic] = Field(description="List of flavors")
    images: List[ImageReadPublic] = Field(description="List of images")
    provider: ProviderReadPublic = Field(description="Provider owning this Project.")
    quotas: List[
        Union[
            ComputeQuotaReadExtendedPublic,
            BlockStorageQuotaReadExtendedPublic,
            NetworkQuotaReadExtendedPublic,
        ]
    ] = Field(description="List of owned quotas.")
    sla: Optional[SLAReadExtendedPublic] = Field(
        default=None, description="SLA involving this Project."
    )

    @classmethod
    def from_orm(cls, obj: Any) -> "ProjectReadExtended":
        """Method to merge public and private flavors, images and networks.

        `obj` is the orm model instance.
        """
        obj.flavors = obj.public_flavors() + obj.private_flavors.all()
        obj.images = obj.public_images() + obj.private_images.all()
        obj.networks = obj.public_networks() + obj.private_networks.all()
        return super().from_orm(obj)
