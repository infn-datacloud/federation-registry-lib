"""Pydantic extended models of the Service supplied by Providers on specific Regions."""
from typing import List

from pydantic import BaseModel, Field

from fed_reg.flavor.schemas import FlavorRead, FlavorReadPublic
from fed_reg.image.schemas import ImageRead, ImageReadPublic
from fed_reg.models import BaseReadPrivateExtended, BaseReadPublicExtended
from fed_reg.network.schemas import NetworkRead, NetworkReadPublic
from fed_reg.project.schemas import ProjectRead, ProjectReadPublic
from fed_reg.provider.schemas import ProviderRead, ProviderReadPublic
from fed_reg.quota.constants import DOC_EXT_PROJ
from fed_reg.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
)
from fed_reg.region.constants import DOC_EXT_PROV
from fed_reg.region.schemas import RegionRead, RegionReadPublic
from fed_reg.service.constants import (
    DOC_EXT_FLAV,
    DOC_EXT_IMAG,
    DOC_EXT_NETW,
    DOC_EXT_QUOTA,
    DOC_EXT_REG,
)
from fed_reg.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)


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
        project (ProjectRead): Target project.
    """

    project: ProjectRead = Field(description=DOC_EXT_PROJ)


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Block Storage Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        project (ProjectReadPublic): Target project.
    """

    project: ProjectReadPublic = Field(description=DOC_EXT_PROJ)


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
        project (ProjectRead): Target project.
    """

    project: ProjectRead = Field(description=DOC_EXT_PROJ)


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Compute Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        project (ProjectReadPublic): Target project.
    """

    project: ProjectReadPublic = Field(description=DOC_EXT_PROJ)


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
        project (ProjectRead): Target project.
    """

    project: ProjectRead = Field(description=DOC_EXT_PROJ)


class NetworkQuotaReadExtendedPublic(NetworkQuotaReadPublic):
    """Model to extend the Network Quota public data read from the DB.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        per_user (str): This limitation should be applied to each user.
        project (ProjectReadPublic): Target project.
    """

    project: ProjectReadPublic = Field(description=DOC_EXT_PROJ)


class BlockStorageServiceReadExtended(BlockStorageServiceRead, BaseReadPrivateExtended):
    """Model to extend the Block Storage Quota data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
        quotas (list of BlockStorageQuotaReadExtended): Quotas pointing to this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)
    quotas: List[BlockStorageQuotaReadExtended] = Field(description=DOC_EXT_QUOTA)


class BlockStorageServiceReadExtendedPublic(
    BlockStorageServiceReadPublic, BaseReadPublicExtended
):
    """Model to extend the Block Storage Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
        quotas (list of BlockStorageQuotaReadExtendedPublic): Quotas pointing to this
            service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)
    quotas: List[BlockStorageQuotaReadExtendedPublic] = Field(description=DOC_EXT_QUOTA)


class ComputeServiceReadExtended(ComputeServiceRead, BaseReadPrivateExtended):
    """Model to extend the Compute Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtendedPublic): Region hosting this service.
        flavors (list of FlavorRead): Supplied flavors.
        images (list of ImageRead): Supplied images.
        quotas (list of ComputeQuotaReadExtended): Quotas pointing to this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)
    quotas: List[ComputeQuotaReadExtended] = Field(description=DOC_EXT_QUOTA)
    flavors: List[FlavorRead] = Field(description=DOC_EXT_FLAV)
    images: List[ImageRead] = Field(description=DOC_EXT_IMAG)


class ComputeServiceReadExtendedPublic(
    ComputeServiceReadPublic, BaseReadPublicExtended
):
    """Model to extend the Compute Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
        flavors (list of FlavorReadPublic): Supplied flavors.
        images (list of ImageReadPublic): Supplied images.
        quotas (list of ComputeQuotaReadExtendedPublic): Quotas pointing to this
            service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)
    quotas: List[ComputeQuotaReadExtendedPublic] = Field(description=DOC_EXT_QUOTA)
    flavors: List[FlavorReadPublic] = Field(description=DOC_EXT_FLAV)
    images: List[ImageReadPublic] = Field(description=DOC_EXT_IMAG)


class IdentityServiceReadExtended(IdentityServiceRead, BaseReadPrivateExtended):
    """Model to extend the Identity Service data read from the DB.

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


class IdentityServiceReadExtendedPublic(
    IdentityServiceReadPublic, BaseReadPublicExtended
):
    """Model to extend the Identity Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)


class NetworkServiceReadExtended(NetworkServiceRead, BaseReadPrivateExtended):
    """Model to extend the Network Service data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
        region (RegionReadExtended): Region hosting this service.
        networks (list of NetworkRead): Supplied networks.
        quotas (list of NetworkQuotaReadExtended): Quotas pointing to this service.
    """

    region: RegionReadExtended = Field(description=DOC_EXT_REG)
    quotas: List[NetworkQuotaReadExtended] = Field(description=DOC_EXT_QUOTA)
    networks: List[NetworkRead] = Field(description=DOC_EXT_NETW)


class NetworkServiceReadExtendedPublic(
    NetworkServiceReadPublic, BaseReadPublicExtended
):
    """Model to extend the Network Service public data read from the DB.

    Attributes:
    ----------
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        region (RegionReadExtendedPublic): Region hosting this service.
        networks (list of NetworkReadPublic): Supplied networks.
        quotas (list of NetworkQuotaReadExtendedPublic): Quotas pointing to this
            service.
    """

    region: RegionReadExtendedPublic = Field(description=DOC_EXT_REG)
    quotas: List[NetworkQuotaReadExtendedPublic] = Field(description=DOC_EXT_QUOTA)
    networks: List[NetworkReadPublic] = Field(description=DOC_EXT_NETW)


class BlockStorageServiceReadSingle(BaseModel):
    __root__: BlockStorageServiceReadExtended | BlockStorageServiceRead | BlockStorageServiceReadExtendedPublic | BlockStorageServiceReadPublic = Field(
        ..., discriminator="schema_type"
    )


class BlockStorageServiceReadMulti(BaseModel):
    __root__: List[BlockStorageServiceReadExtended] | List[
        BlockStorageServiceRead
    ] | List[BlockStorageServiceReadExtendedPublic] | List[
        BlockStorageServiceReadPublic
    ] = Field(..., discriminator="schema_type")


class ComputeServiceReadSingle(BaseModel):
    __root__: ComputeServiceReadExtended | ComputeServiceRead | ComputeServiceReadExtendedPublic | ComputeServiceReadPublic = Field(
        ..., discriminator="schema_type"
    )


class ComputeServiceReadMulti(BaseModel):
    __root__: List[ComputeServiceReadExtended] | List[ComputeServiceRead] | List[
        ComputeServiceReadExtendedPublic
    ] | List[ComputeServiceReadPublic] = Field(..., discriminator="schema_type")


class IdentityServiceReadSingle(BaseModel):
    __root__: IdentityServiceReadExtended | IdentityServiceRead | IdentityServiceReadExtendedPublic | IdentityServiceReadPublic = Field(
        ..., discriminator="schema_type"
    )


class IdentityServiceReadMulti(BaseModel):
    __root__: List[IdentityServiceReadExtended] | List[IdentityServiceRead] | List[
        IdentityServiceReadExtendedPublic
    ] | List[IdentityServiceReadPublic] = Field(..., discriminator="schema_type")


class NetworkServiceReadSingle(BaseModel):
    __root__: NetworkServiceReadExtended | NetworkServiceRead | NetworkServiceReadExtendedPublic | NetworkServiceReadPublic = Field(
        ..., discriminator="schema_type"
    )


class NetworkServiceReadMulti(BaseModel):
    __root__: List[NetworkServiceReadExtended] | List[NetworkServiceRead] | List[
        NetworkServiceReadExtendedPublic
    ] | List[NetworkServiceReadPublic] = Field(..., discriminator="schema_type")
