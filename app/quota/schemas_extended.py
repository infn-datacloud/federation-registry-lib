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
    """Model to extend the Region data read from the DB.

    Add the provider hosting this region.
    """

    provider: ProviderRead


class RegionReadExtendedPublic(RegionReadPublic):
    """Model to extend the Region public data read from the DB.

    Add the provider hosting this region.
    """

    provider: ProviderReadPublic


class BlockStorageServiceReadExtended(BlockStorageServiceRead):
    """Model to extend the Block Storage Service data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadExtended = Field(description="Region hosting this service")


class BlockStorageServiceReadExtendedPublic(BlockStorageServiceReadPublic):
    """Model to extend the Block Storage Service public data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadExtended = Field(description="Region hosting this service")


class ComputeServiceReadExtended(ComputeServiceRead):
    """Model to extend the Compute Service data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadExtended = Field(description="Region hosting this service")


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic):
    """Model to extend the Compute Service public data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadExtended = Field(description="Region hosting this service")


class NetworkServiceReadExtended(NetworkServiceRead):
    """Model to extend the Network Service data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadExtended = Field(description="Region hosting this service")


class NetworkServiceReadExtendedPublic(NetworkServiceReadPublic):
    """Model to extend the Network Service public data read from the DB.

    Add the region hosting it.
    """

    region: RegionReadExtended = Field(description="Region hosting this service")


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead):
    """Model to extend the Block Storage Quota data read from the DB.

    Add the target project and block storage service.
    """

    project: ProjectRead
    service: BlockStorageServiceReadExtended


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic):
    """Model to extend the Block Storage Quota public data read from the DB.

    Add the target project and block storage service.
    """

    project: ProjectReadPublic
    service: BlockStorageServiceReadExtendedPublic


class ComputeQuotaReadExtended(ComputeQuotaRead):
    """Model to extend the Compute Quota data read from the DB.

    Add the target project and compute service.
    """

    project: ProjectRead
    service: ComputeServiceReadExtended


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic):
    """Model to extend the Compute Quota public data read from the DB.

    Add the target project and compute service.
    """

    project: ProjectReadPublic
    service: ComputeServiceReadExtendedPublic


class NetworkQuotaReadExtended(NetworkQuotaRead):
    """Model to extend the Network Quota data read from the DB.

    Add the target project and network service.
    """

    project: ProjectRead
    service: NetworkServiceReadExtended


class NetworkQuotaReadExtendedPublic(NetworkQuotaReadPublic):
    """Model to extend the Network Quota public data read from the DB.

    Add the target project and network service.
    """

    project: ProjectReadPublic
    service: NetworkServiceReadExtendedPublic
