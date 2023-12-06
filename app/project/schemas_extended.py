"""Pydantic extended models of the Project owned by a Provider."""
from typing import List, Optional, Union

from pydantic import Field

from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.image.schemas import ImageRead, ImageReadPublic
from app.network.schemas import NetworkRead, NetworkReadPublic
from app.project.models import Project
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

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionRead): Region hosting this service.
    """

    region: RegionRead = Field(description="Region hosting this service.")


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the Block Storage Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadPublic): Region hosting this service.
    """

    region: RegionReadPublic = Field(description="Region hosting this service.")


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionRead): Region hosting this service.
    """

    region: RegionRead = Field(description="Region hosting this service.")


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadPublic): Region hosting this service.
    """

    region: RegionReadPublic = Field(description="Region hosting this service.")


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionRead): Region hosting this service.
    """

    region: RegionRead = Field(description="Region hosting this service.")


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadPublic): Region hosting this service.
    """

    region: RegionReadPublic = Field(description="Region hosting this service.")


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    """Model to extend the Block Storage Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
        service (BlockStorageServiceReadExtended): Target block storage service.
    """

    service: BlockStorageServiceReadExtended = Field(
        description="A generic Quota applies to only one generic Service."
    )


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Block Storage Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        service (BlockStorageServiceReadExtendedPublic): Target block storage service.
    """

    service: BlockStorageServiceReadExtendedPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class ComputeQuotaReadExtended(ComputeQuotaRead):
    """Model to extend the Compute Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        cores (int | None): Number of max usable cores.
        instance (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
        service (ComputeServiceReadExtended): Target compute service.
    """

    service: ComputeServiceReadExtended = Field(
        description="A generic Quota applies to only one generic Service."
    )


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Compute Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        service (ComputeServiceReadExtendedPublic): Target compute service.
    """

    service: ComputeServiceReadExtendedPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class NetworkQuotaReadExtended(NetworkQuotaRead):
    """Model to extend the Network Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        port (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
        service (NetworkServiceReadExtended): Target network service.
    """

    service: NetworkServiceReadExtended = Field(
        description="A generic Quota applies to only one generic Service."
    )


class NetworkQuotaReadExtendedPublic(NetworkQuotaReadPublic):
    """Model to extend the Network Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        service (NetworkServiceReadExtendedPublic): Target network service.
    """

    service: NetworkServiceReadExtendedPublic = Field(
        description="A generic Quota applies to only one generic Service."
    )


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderRead): Identity provider owning this user
            group.
    """

    identity_provider: IdentityProviderRead = Field(
        description="Identity Provider owning this User Group."
    )


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group public data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderReadPublic): Identity provider owning this
            user group.
    """

    identity_provider: IdentityProviderReadPublic = Field(
        description="Identity Provider owning this User Group."
    )


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
        user_group (UserGroupReadExtended): Target user group.
    """

    user_group: UserGroupReadExtended = Field(description="Involved User Group.")


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA public data read from the DB.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        user_group (UserGroupReadExtendedPublic): Target user group.
    """

    user_group: UserGroupReadExtendedPublic = Field(description="Involved User Group.")


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        provider (ProviderRead): Hosting provider.
        sla (SLAReadExtended | None): SLA pointing to this project.
        flavors (list of FlavorRead): Private and public accessible flavors.
        images (list of ImageRead): Private and public accessible images.
        networks (list of NetworkRead): Private and public accessible networks.
        quotas (list of Quota): List of owned quotas pointing to the corresponding
            service (block-storage, compute and network type).
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
    def from_orm(cls, obj: Project) -> "ProjectReadExtended":
        """Method to merge public and private flavors, images and networks.

        `obj` is the orm model instance.
        """
        obj.flavors = obj.public_flavors() + obj.private_flavors.all()
        obj.images = obj.public_images() + obj.private_images.all()
        obj.networks = obj.public_networks() + obj.private_networks.all()
        return super().from_orm(obj)


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        provider (ProviderReadPublic): Hosting provider.
        sla (SLAReadExtendedPublic | None): SLA pointing to this project.
        flavors (list of FlavorReadPublic): Private and public accessible flavors.
        images (list of ImageReadPublic): Private and public accessible images.
        networks (list of NetworkReadPublic): Private and public accessible networks.
        quotas (list of QuotaPublic): List of owned quotas pointing to the corresponding
            service (block-storage, compute and network type).
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
    def from_orm(cls, obj: Project) -> "ProjectReadExtended":
        """Method to merge public and private flavors, images and networks.

        `obj` is the orm model instance.
        """
        obj.flavors = obj.public_flavors() + obj.private_flavors.all()
        obj.images = obj.public_images() + obj.private_images.all()
        obj.networks = obj.public_networks() + obj.private_networks.all()
        return super().from_orm(obj)
