"""Pydantic extended models of the Project owned by a Provider."""

from pydantic import BaseModel, Field

from fedreg.auth_method.schemas import AuthMethodRead
from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.flavor.schemas import FlavorRead, FlavorReadPublic
from fedreg.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fedreg.image.schemas import ImageRead, ImageReadPublic
from fedreg.network.schemas import NetworkRead, NetworkReadPublic
from fedreg.project.constants import (
    DOC_EXT_FLAV,
    DOC_EXT_IMAG,
    DOC_EXT_NETW,
    DOC_EXT_PROV,
    DOC_EXT_QUOTA,
    DOC_EXT_SLA,
)
from fedreg.project.models import Project
from fedreg.project.schemas import ProjectRead, ProjectReadPublic
from fedreg.provider.constants import DOC_EXT_AUTH_METH
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.quota.constants import DOC_EXT_SERV
from fedreg.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    ObjectStoreQuotaRead,
    ObjectStoreQuotaReadPublic,
)
from fedreg.region.models import Region
from fedreg.region.schemas import RegionRead, RegionReadPublic
from fedreg.service.constants import DOC_EXT_REG
from fedreg.service.enum import ServiceType
from fedreg.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    ObjectStoreServiceRead,
    ObjectStoreServiceReadPublic,
)
from fedreg.sla.constants import DOC_EXT_GROUP
from fedreg.sla.schemas import SLARead, SLAReadPublic
from fedreg.user_group.constants import DOC_EXT_IDP
from fedreg.user_group.schemas import UserGroupRead, UserGroupReadPublic


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

    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the Block Storage Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadPublic): Region hosting this service.
    """

    region: RegionReadPublic = Field(description=DOC_EXT_REG)


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

    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadPublic): Region hosting this service.
    """

    region: RegionReadPublic = Field(description=DOC_EXT_REG)


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

    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadPublic): Region hosting this service.
    """

    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class ObjectStoreServiceReadExtended(ObjectStoreServiceRead):
    """Model to extend the Object Storage Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionRead): Region hosting this service.
    """

    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class ObjectStoreServiceReadExtendedPublic(ObjectStoreServiceReadPublic):
    """Model to extend the Object Storage Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadPublic): Region hosting this service.
    """

    region: RegionReadPublic = Field(description=DOC_EXT_REG)


class NetworkReadExtended(NetworkRead):
    """Model to extend the Network data read from the DB.

    Attributes:
    ----------
        uid (int):  unique ID.
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        is_shared (bool): Public or private Network.
        is_router_external (bool): Network with access to outside networks. External
            network.
        is_default (bool): Network to use as default.
        mtu (int | None): Metric transmission unit (B).
        proxy_host (str | None): Proxy IP address.
        proxy_user (str | None): Proxy username.
        tags (list of str): list of tags associated to this Network.
        service (NetworkServiceReadExtendedPublic): Target service. Same type of quota.
    """

    service: NetworkServiceReadExtended = Field(description=DOC_EXT_SERV)


class NetworkReadExtendedPublic(NetworkReadPublic):
    """Model to extend the Network public data read from the DB.

    Attributes:
    ----------
        uid (int):  unique ID.
        description (str): Brief description.
        name (str): Network name in the Provider.
        uuid (str): Network unique ID in the Provider
        service (NetworkServiceReadExtendedPublic): Target service. Same type of quota.
    """

    service: NetworkServiceReadExtendedPublic = Field(description=DOC_EXT_SERV)


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


class ProviderReadWithAuthMethod(ProviderReadPublic):
    """Model to extend the Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        relationship (AuthMethodRead): Authentication method used by the target
            provider to connect.
    """

    relationship: AuthMethodRead = Field(description=DOC_EXT_AUTH_METH)


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): value of the key from which retrieve
            the user group name from an authentication token.
        providers (list of ProviderReadWithAuthMethod): Supported providers. Since we
            already show the complete data of the provider in another point we are ok
            to show just a shrunk version here.
    """

    providers: list[ProviderReadWithAuthMethod] = Field(description=DOC_EXT_PROV)


class IdentityProviderReadExtendedPublic(IdentityProviderReadPublic):
    """Model to extend the Identity Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        providers (list of ProviderReadWithAuthMethod): Supported providers.
    """

    providers: list[ProviderReadWithAuthMethod] = Field(description=DOC_EXT_PROV)


class UserGroupReadExtended(UserGroupRead):
    """Model to extend the User Group data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderReadExtended): Identity provider owning this
            user group.
    """

    identity_provider: IdentityProviderReadExtended = Field(description=DOC_EXT_IDP)


class UserGroupReadExtendedPublic(UserGroupReadPublic):
    """Model to extend the User Group public data read from the DB.

    Attributes:
    ----------
        uid (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
        identity_provider (IdentityProviderReadExtendedPublic): Identity provider
            owning this user group.
    """

    identity_provider: IdentityProviderReadExtendedPublic = Field(
        description=DOC_EXT_IDP
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

    user_group: UserGroupReadExtended = Field(description=DOC_EXT_GROUP)


class SLAReadExtendedPublic(SLAReadPublic):
    """Model to extend the SLA public data read from the DB.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        user_group (UserGroupReadExtendedPublic): Target user group.
    """

    user_group: UserGroupReadExtendedPublic = Field(description=DOC_EXT_GROUP)


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        identity_services (list of IdentityServiceReadPublic): Available identity
            services.
    """

    identity_services: list[IdentityServiceReadPublic] = Field(
        default_factory=list, description="Available identity services list"
    )

    @classmethod
    def from_orm(cls, obj: Region) -> "RegionReadExtended":
        """Method to merge public and private flavors, images and networks.

        `obj` is the orm model instance.
        """
        obj.identity_services = obj.services.filter(type=ServiceType.IDENTITY.value)
        return super().from_orm(obj)


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        identity_services (list of IdentityServiceReadPublic): Available identity
            services.
    """

    identity_services: list[IdentityServiceReadPublic] = Field(
        default_factory=list, description="Available identity services list"
    )

    @classmethod
    def from_orm(cls, obj: Region) -> "RegionReadExtendedPublic":
        """Method to merge public and private flavors, images and networks.

        `obj` is the orm model instance.
        """
        obj.identity_services = obj.services.filter(type=ServiceType.IDENTITY.value)
        return super().from_orm(obj)


class ProviderReadExtended(ProviderRead):
    """Model to extend the Provider data read from the DB.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): list of maintainers emails.
        regions (list of RegionReadWithIdentityService): Supplied regions.
    """

    regions: list[RegionReadExtended] = Field(
        default_factory=list, description=DOC_EXT_REG
    )


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): list of maintainers emails.
        regions (list of RegionReadWithIdentityService): Supplied regions.
    """

    regions: list[RegionReadExtendedPublic] = Field(
        default_factory=list, description=DOC_EXT_REG
    )


class ProjectReadExtended(BaseReadPrivateExtended, ProjectRead):
    """Model to extend the Project data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        provider (ProviderRead): Provider owning this project.
        sla (SLAReadExtended | None): SLA pointing to this project.
        flavors (list of FlavorRead): Private and public accessible flavors.
        images (list of ImageRead): Private and public accessible images.
        networks (list of NetworkReadExtended): Private and public accessible networks.
        quotas (list of Quota): list of owned quotas pointing to the corresponding
            service (block-storage, compute and network type).
    """

    flavors: list[FlavorRead] = Field(default_factory=list, description=DOC_EXT_FLAV)
    images: list[ImageRead] = Field(default_factory=list, description=DOC_EXT_IMAG)
    networks: list[NetworkReadExtended] = Field(
        default_factory=list, description=DOC_EXT_NETW
    )
    provider: ProviderReadExtended = Field(description=DOC_EXT_PROV)
    quotas: list[
        BlockStorageQuotaReadExtended
        | ComputeQuotaReadExtended
        | NetworkQuotaReadExtended
        | ObjectStoreQuotaReadExtended
    ] = Field(default_factory=list, description=DOC_EXT_QUOTA)
    sla: SLAReadExtended | None = Field(default=None, description=DOC_EXT_SLA)

    @classmethod
    def from_orm(cls, obj: Project) -> "ProjectReadExtended":
        """Method to merge shared and private flavors, images and networks.

        `obj` is the orm model instance.
        """
        obj.flavors = obj.shared_flavors() + obj.private_flavors.all()
        obj.images = obj.shared_images() + obj.private_images.all()
        obj.networks = obj.shared_networks() + obj.private_networks.all()
        return super().from_orm(obj)


class ProjectReadExtendedPublic(BaseReadPublicExtended, ProjectReadPublic):
    """Model to extend the Project public data read from the DB.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
        provider (ProviderReadPublic): Provider owning this project.
        sla (SLAReadExtendedPublic | None): SLA pointing to this project.
        flavors (list of FlavorReadPublic): Private and public accessible flavors.
        images (list of ImageReadPublic): Private and public accessible images.
        networks (list of NetworkReadExtendedPublic): Private and public accessible
            networks.
        quotas (list of QuotaPublic): list of owned quotas pointing to the corresponding
            service (block-storage, compute and network type).
    """

    flavors: list[FlavorReadPublic] = Field(
        default_factory=list, description=DOC_EXT_FLAV
    )
    images: list[ImageReadPublic] = Field(
        default_factory=list, description=DOC_EXT_IMAG
    )
    networks: list[NetworkReadExtendedPublic] = Field(
        default_factory=list, description=DOC_EXT_NETW
    )
    provider: ProviderReadExtendedPublic = Field(description=DOC_EXT_PROV)
    quotas: list[
        BlockStorageQuotaReadExtendedPublic
        | ComputeQuotaReadExtendedPublic
        | NetworkQuotaReadExtendedPublic
        | ObjectStoreQuotaReadExtendedPublic
    ] = Field(default_factory=list, description=DOC_EXT_QUOTA)
    sla: SLAReadExtendedPublic | None = Field(default=None, description=DOC_EXT_SLA)

    @classmethod
    def from_orm(cls, obj: Project) -> "ProjectReadExtendedPublic":
        """Method to merge shared and private flavors, images and networks.

        `obj` is the orm model instance.
        """
        obj.flavors = obj.shared_flavors() + obj.private_flavors.all()
        obj.images = obj.shared_images() + obj.private_images.all()
        obj.networks = obj.shared_networks() + obj.private_networks.all()
        return super().from_orm(obj)


class ProjectReadSingle(BaseModel):
    __root__: (
        ProjectReadExtended
        | ProjectRead
        | ProjectReadExtendedPublic
        | ProjectReadPublic
    ) = Field(..., discriminator="schema_type")


class ProjectReadMulti(BaseModel):
    __root__: (
        list[ProjectReadExtended]
        | list[ProjectRead]
        | list[ProjectReadExtendedPublic]
        | list[ProjectReadPublic]
    ) = Field(..., discriminator="schema_type")
