"""Pydantic extended models of the Service supplied by Providers on specific Regions."""
from typing import List

from pydantic import Field

from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.image.schemas import ImageRead, ImageReadPublic
from app.network.schemas import NetworkReadPublic
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
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)


class RegionReadExtended(RegionRead):
    """Model to extend the Region data read from the DB.

    Add the provider hosting this region.
    """

    provider: ProviderRead = Field(description="Provider")


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Add the provider hosting this region.
    """

    provider: ProviderReadPublic = Field(description="Provider")


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    """Model to extend the Block Storage Quota data read from the DB.

    Add the target project.
    """

    project: ProjectRead


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Block Storage Quota public data read from the DB.

    Add the target project.
    """

    project: ProjectReadPublic


class ComputeQuotaReadExtended(ComputeQuotaRead):
    """Model to extend the Compute Quota data read from the DB.

    Add the target project.
    """

    project: ProjectRead


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Compute Quota public data read from the DB.

    Add the target project.
    """

    project: ProjectReadPublic


class NetworkQuotaReadExtended(NetworkQuotaRead):
    """Model to extend the Network Quota data read from the DB.

    Add the target project.
    """

    project: ProjectRead


class NetworkQuotaReadExtendedPublic(NetworkQuotaReadPublic):
    """Model to extend the Network Quota public data read from the DB.

    Add the target project.
    """

    project: ProjectReadPublic


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    """Model to extend the Block Storage Quota data read from the DB.

    Add the target project.
    """

    quotas: List[BlockStorageQuotaReadExtended] = Field(description="List of quotas.")
    region: RegionReadExtended


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the Block Storage Service public data read from the DB.

    Add the region hosting it and the list of related quotas.
    """

    quotas: List[BlockStorageQuotaReadExtendedPublic] = Field(
        description="List of quotas."
    )
    region: RegionReadExtendedPublic


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB.

    Add the region hosting it, the list of related quotas and the list of supplied
    flavors and images.
    """

    flavors: List[FlavorRead] = Field(description="List of owned Flavors.")
    images: List[ImageRead] = Field(description="List of owned Images.")
    quotas: List[ComputeQuotaReadExtended] = Field(description="List of quotas.")
    region: RegionReadExtended


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Add the region hosting it, the list of related quotas and the list of supplied
    flavors and images.
    """

    flavors: List[FlavorReadPublic] = Field(description="List of owned Flavors.")
    images: List[ImageReadPublic] = Field(description="List of owned Images.")
    quotas: List[ComputeQuotaReadExtendedPublic] = Field(description="List of quotas.")
    region: RegionReadExtendedPublic


class IdentityServiceReadExtended(IdentityServiceRead):
    """Model to extend the Identity Service data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadExtended


class IdentityServiceReadExtendedPublic(IdentityServiceReadPublic):
    """Model to extend the Identity Service public data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadExtendedPublic


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB.

    Add the region hosting it, the list of related quotas and the list of supplied
    networks.
    """

    networks: List[NetworkReadPublic] = Field(description="List of owned Networks.")
    region: RegionReadExtended
    quotas: List[NetworkQuotaReadExtended] = Field(description="List of quotas.")


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Add the region hosting it, the list of related quotas and the list of supplied
    networks.
    """

    networks: List[NetworkReadPublic] = Field(description="List of owned Networks.")
    region: RegionReadExtendedPublic
    quotas: List[NetworkQuotaReadExtendedPublic] = Field(description="List of quotas.")
