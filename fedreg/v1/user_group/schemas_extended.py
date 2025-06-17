"""Pydantic extended models of the User Group owned by an Identity Provider."""

from pydantic import Field

from fedreg.v1.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.v1.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fedreg.v1.project.constants import DOC_EXT_PROV, DOC_EXT_QUOTA
from fedreg.v1.project.schemas import ProjectRead, ProjectReadPublic
from fedreg.v1.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.v1.quota.constants import DOC_EXT_SERV
from fedreg.v1.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    ObjectStoreQuotaRead,
    ObjectStoreQuotaReadPublic,
)
from fedreg.v1.region.schemas import RegionReadPublic
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
from fedreg.v1.sla.constants import DOC_EXT_PROJ
from fedreg.v1.sla.schemas import SLARead, SLAReadPublic
from fedreg.v1.user_group.constants import DOC_EXT_IDP, DOC_EXT_SLA
from fedreg.v1.user_group.schemas import UserGroupRead, UserGroupReadPublic


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
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
        service (BlockStorageServiceReadExtended): Target service. Same type of quota.
    """

    service: BlockStorageServiceReadExtended = Field(description=DOC_EXT_SERV)


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Block Storage Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        service (BlockStorageServiceReadExtendedPublic): Target service. Same type of
            quota.
    """

    service: BlockStorageServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)


class ComputeServiceReadExtended(ComputeServiceRead):
    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class ComputeQuotaReadExtended(ComputeQuotaRead):
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
        service (ComputeServiceReadExtended): Target service. Same type of quota.
    """

    service: ComputeServiceReadExtended = Field(description=DOC_EXT_SERV)


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Compute Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        service (ComputeServiceReadExtendedPublic): Target service. Same type of quota.
    """

    service: ComputeServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)


class NetworkServiceReadExtended(NetworkServiceRead):
    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class NetworkQuotaReadExtended(NetworkQuotaRead):
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
        service (NetworkServiceReadExtended): Target service. Same type of quota.
    """

    service: NetworkServiceReadExtended = Field(description=DOC_EXT_SERV)


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class NetworkQuotaReadExtendedPublic(NetworkQuotaReadPublic):
    """Model to extend the Network Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        service (NetworkServiceReadExtendedPublic): Target service. Same type of quota.
    """

    service: NetworkServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)


class ObjectStoreServiceReadExtended(ObjectStoreServiceRead):
    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class ObjectStoreQuotaReadExtended(ObjectStoreQuotaRead):
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
        service (ObjectStoreServiceReadExtended): Target service. Same type of quota.
    """

    service: ObjectStoreServiceReadExtended = Field(description=DOC_EXT_SERV)


class ObjectStoreServiceReadExtendedPublic(ObjectStoreServiceReadPublic):
    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class ObjectStoreQuotaReadExtendedPublic(ObjectStoreQuotaReadPublic):
    """Model to extend the Object Storage Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        service (ObjectStoreServiceReadExtendedPublic): Target service. Same type of
            quota.
    """

    service: ObjectStoreServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)


class ProjectReadExtended(ProjectRead):
    """Model to extend the Project data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        provider (ProviderRead): Hosting provider.
    """

    provider: ProviderRead = Field(description=DOC_EXT_PROV)
    quotas: list[
        ComputeQuotaReadExtended
        | BlockStorageQuotaReadExtended
        | NetworkQuotaReadExtended
        | ObjectStoreQuotaReadExtended
    ] = Field(description=DOC_EXT_QUOTA)


class ProjectReadExtendedPublic(ProjectReadPublic):
    """Model to extend the Project public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        provider (ProviderReadPublic): Hosting provider.
    """

    provider: ProviderReadPublic = Field(description=DOC_EXT_PROV)
    quotas: list[
        ComputeQuotaReadExtendedPublic
        | BlockStorageQuotaReadExtendedPublic
        | NetworkQuotaReadExtendedPublic
        | ObjectStoreQuotaReadExtendedPublic
    ] = Field(description=DOC_EXT_QUOTA)


class SLAReadExtended(SLARead):
    """Model to extend the SLA data read from the DB.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
        projects (list of ProjectReadExtended): Target projects.
    """

    projects: list[ProjectReadExtended] = Field(description=DOC_EXT_PROJ)


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA public data read from the DB.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        projects (list of ProjectReadExtended): Target projects.
    """

    projects: list[ProjectReadExtendedPublic] = Field(description=DOC_EXT_PROJ)


class UserGroupReadExtended(BaseReadPrivateExtended, UserGroupRead):
    """Model to extend the User Group data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderRead): Identity provider owning this
            user group.
        slas (list of SLAReadExtended): Owned SLAs.
    """

    identity_provider: IdentityProviderRead = Field(description=DOC_EXT_IDP)
    slas: list[SLAReadExtended] = Field(default_factory=list, description=DOC_EXT_SLA)


class UserGroupReadExtendedPublic(BaseReadPublicExtended, UserGroupReadPublic):
    """Model to extend the User Group public data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderReadPublic): Identity provider owning this
            user group.
        slas (list of SLAReadExtendedPublic): Owned SLAs.
    """

    identity_provider: IdentityProviderReadPublic = Field(description=DOC_EXT_IDP)
    slas: list[SLAReadExtendedPublic] = Field(
        default_factory=list, description=DOC_EXT_SLA
    )
