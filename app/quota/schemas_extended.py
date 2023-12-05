"""Pydantic extended models of the Resource limitations for Projects on Services."""
from pydantic import Field

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


class RegionReadExtended(RegionRead):
    provider: ProviderRead


class RegionReadExtendedPublic(RegionReadPublic):
    provider: ProviderReadPublic


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    region: RegionReadExtended = Field(description="Region hosting this service")


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    region: RegionReadExtended = Field(description="Region hosting this service")


class ComputeServiceReadExtended(ComputeServiceRead):
    region: RegionReadExtended = Field(description="Region hosting this service")


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    region: RegionReadExtended = Field(description="Region hosting this service")


class NetworkServiceReadExtended(NetworkServiceRead):
    region: RegionReadExtended = Field(description="Region hosting this service")


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    region: RegionReadExtended = Field(description="Region hosting this service")


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    project: ProjectRead
    service: BlockStorageServiceReadExtended


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    project: ProjectReadPublic
    service: BlockStorageServiceReadExtendedPublic


class ComputeQuotaReadExtended(ComputeQuotaRead):
    project: ProjectRead
    service: ComputeServiceReadExtended


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    project: ProjectReadPublic
    service: ComputeServiceReadExtendedPublic


class NetworkQuotaReadExtended(NetworkQuotaRead):
    project: ProjectRead
    service: NetworkServiceReadExtended


class NetworkQuotaReadExtendedPublic(NetworkQuotaReadPublic):
    project: ProjectReadPublic
    service: NetworkServiceReadExtendedPublic
