from typing import List, Optional

from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.image.schemas import ImageRead, ImageReadPublic
from app.location.schemas import LocationRead, LocationReadPublic
from app.network.schemas import NetworkReadPublic
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
    KeystoneServiceRead,
    KeystoneServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)
from pydantic import Field


class RegionReadExtended(RegionRead):
    """Model to extend a Service with the hosting region."""

    location: Optional[LocationRead] = Field(
        default=None, description="Provider location."
    )
    provider: ProviderRead = Field(description="Provider")


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend a Service with the hosting region."""

    location: Optional[LocationReadPublic] = Field(
        default=None, description="Provider location."
    )
    provider: ProviderReadPublic = Field(description="Provider")


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""

    project: ProjectRead


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""

    project: ProjectReadPublic


class ComputeQuotaReadExtended(ComputeQuotaRead):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""

    project: ProjectRead


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""

    project: ProjectReadPublic


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    """Model to extend the BlockStorage Service data read from the DB with the
    lists of related items for authenticated users."""

    quotas: List[BlockStorageQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas.",
    )
    region: RegionReadExtended


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the BlockStorage Service data read from the DB with the
    lists of related items for non-authenticated users."""

    quotas: List[BlockStorageQuotaReadExtendedPublic] = Field(
        default_factory=list,
        description="List of quotas.",
    )
    region: RegionReadExtendedPublic


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB with the lists
    of related items for authenticated users."""

    flavors: List[FlavorRead] = Field(
        default_factory=list, description="List of owned Flavors."
    )
    images: List[ImageRead] = Field(
        default_factory=list, description="List of owned Images."
    )
    quotas: List[ComputeQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas.",
    )
    region: RegionReadExtended


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service data read from the DB with the lists
    of related items for non-authenticated users."""

    flavors: List[FlavorReadPublic] = Field(
        default_factory=list, description="List of owned Flavors."
    )
    images: List[ImageReadPublic] = Field(
        default_factory=list, description="List of owned Images."
    )
    quotas: List[ComputeQuotaReadExtendedPublic] = Field(
        default_factory=list,
        description="List of quotas.",
    )
    region: RegionReadExtendedPublic


class KeystoneServiceReadExtended(KeystoneServiceRead):
    """Model to extend the Keystone Service data read from the DB with the
    lists of related items for authenticated users."""

    region: RegionReadExtended


class KeystoneServiceReadExtendedPublic(KeystoneServiceReadPublic):
    """Model to extend the Keystone Service data read from the DB with the
    lists of related items for non-authenticated users."""

    region: RegionReadExtendedPublic


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB with the lists
    of related items for authenticated users."""

    networks: List[NetworkReadPublic] = Field(
        default_factory=list, description="List of owned Networks."
    )
    region: RegionReadExtended


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service data read from the DB with the lists
    of related items for non-authenticated users."""

    networks: List[NetworkReadPublic] = Field(
        default_factory=list, description="List of owned Networks."
    )
    region: RegionReadExtendedPublic
