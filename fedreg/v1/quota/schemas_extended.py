"""Pydantic extended models of the Resource limitations for Projects on Services."""

from pydantic import Field

from fedreg.v1.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.v1.project.schemas import ProjectRead, ProjectReadPublic
from fedreg.v1.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.v1.quota.constants import DOC_EXT_PROJ, DOC_EXT_SERV
from fedreg.v1.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    ObjectStoreQuotaRead,
    ObjectStoreQuotaReadPublic,
    StorageClassQuotaRead,
    StorageClassQuotaReadPublic,
)
from fedreg.v1.region.constants import DOC_EXT_PROV
from fedreg.v1.region.schemas import RegionRead, RegionReadPublic
from fedreg.v1.service.constants import DOC_EXT_REG
from fedreg.v1.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    ObjectStoreServiceRead,
    ObjectStoreServiceReadPublic,
)
from fedreg.v1.storageclass.schemas import StorageClassRead, StorageClassReadPublic


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderRead): Provider hosting target region.
    """

    provider: ProviderRead = Field(description=DOC_EXT_PROV)


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        provider (ProviderReadPublic): Provider hosting target region.
    """

    provider: ProviderReadPublic = Field(description=DOC_EXT_PROV)


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    """Model to extend the Block Storage Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the Block Storage Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)


class ObjectStoreServiceReadExtended(ObjectStoreServiceRead):
    """Model to extend the Object Storage Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)


class ObjectStoreServiceReadExtendedPublic(ObjectStoreServiceReadPublic):
    """Model to extend the Object Storage Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)


class StorageClassReadExtended(StorageClassRead):
    """Model to extend the Network Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
    """

    service: BlockStorageServiceReadExtended = Field(description=DOC_EXT_REG)


class StorageClassReadExtendedPublic(StorageClassReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    service: BlockStorageServiceReadExtendedPublic = Field(description=DOC_EXT_REG)


class BlockStorageQuotaReadExtended(BaseReadPrivateExtended, BlockStorageQuotaRead):
    """Model to extend the Block Storage Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
        project (ProjectRead): Target project.
        service (BlockStorageServiceReadExtended): Target block storage service.
    """

    project: ProjectRead = Field(description=DOC_EXT_PROJ)
    service: BlockStorageServiceReadExtended = Field(description=DOC_EXT_SERV)


class BlockStorageQuotaReadExtendedPublic(
    BaseReadPublicExtended, BlockStorageQuotaReadPublic
):
    """Model to extend the Block Storage Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        project (ProjectReadPublic): Target project.
        service (BlockStorageServiceReadExtendedPublic): Target block storage service.
    """

    project: ProjectReadPublic = Field(description=DOC_EXT_PROJ)
    service: BlockStorageServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)


class StorageClassQuotaReadExtended(BaseReadPrivateExtended, StorageClassQuotaRead):
    """Model to extend the Block Storage Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
        project (ProjectRead): Target project.
        service (StorageClassServiceReadExtended): Target block storage service.
    """

    project: ProjectRead = Field(description=DOC_EXT_PROJ)
    service: StorageClassReadExtended = Field(description=DOC_EXT_SERV)


class StorageClassQuotaReadExtendedPublic(
    BaseReadPublicExtended, StorageClassQuotaReadPublic
):
    """Model to extend the Block Storage Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        project (ProjectReadPublic): Target project.
        service (StorageClassServiceReadExtendedPublic): Target block storage service.
    """

    project: ProjectReadPublic = Field(description=DOC_EXT_PROJ)
    service: StorageClassReadExtendedPublic = Field(description=DOC_EXT_SERV)


class ComputeQuotaReadExtended(BaseReadPrivateExtended, ComputeQuotaRead):
    """Model to extend the Compute Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        cores (int | None): Number of max usable cores.
        instance (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
        project (ProjectRead): Target project.
        service (ComputeServiceReadExtended): Target compute service.
    """

    project: ProjectRead = Field(description=DOC_EXT_PROJ)
    service: ComputeServiceReadExtended = Field(description=DOC_EXT_SERV)


class ComputeQuotaReadExtendedPublic(BaseReadPublicExtended, ComputeQuotaReadPublic):
    """Model to extend the Compute Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        project (ProjectReadPublic): Target project.
        service (ComputeServiceReadExtendedPublic): Target compute service.
    """

    project: ProjectReadPublic = Field(description=DOC_EXT_PROJ)
    service: ComputeServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)


class NetworkQuotaReadExtended(BaseReadPrivateExtended, NetworkQuotaRead):
    """Model to extend the Network Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        ports (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
        project (ProjectRead): Target project.
        service (NetworkServiceReadExtended): Target network service.
    """

    project: ProjectRead = Field(description=DOC_EXT_PROJ)
    service: NetworkServiceReadExtended = Field(description=DOC_EXT_SERV)


class NetworkQuotaReadExtendedPublic(BaseReadPublicExtended, NetworkQuotaReadPublic):
    """Model to extend the Network Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        project (ProjectReadPublic): Target project.
        service (NetworkServiceReadExtendedPublic): Target network service.
    """

    project: ProjectReadPublic = Field(description=DOC_EXT_PROJ)
    service: NetworkServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)


class ObjectStoreQuotaReadExtended(BaseReadPrivateExtended, ObjectStoreQuotaRead):
    """Model to extend the Object Storage Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        bytes (int): Maximum number of allowed bytes.
        containers (int): Maximum number of allowed containers.
        objects (int): Maximum number of allowed objects.
        project (ProjectRead): Target project.
        service (ObjectStoreServiceReadExtended): Target block storage service.
    """

    project: ProjectRead = Field(description=DOC_EXT_PROJ)
    service: ObjectStoreServiceReadExtended = Field(description=DOC_EXT_SERV)


class ObjectStoreQuotaReadExtendedPublic(
    BaseReadPublicExtended, ObjectStoreQuotaReadPublic
):
    """Model to extend the Object Storage Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        project (ProjectReadPublic): Target project.
        service (ObjectStoreServiceReadExtendedPublic): Target block storage service.
    """

    project: ProjectReadPublic = Field(description=DOC_EXT_PROJ)
    service: ObjectStoreServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)
