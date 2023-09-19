from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    QuotaRead,
    QuotaReadPublic,
)
from app.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
)


class ProjectReadExtended(ProjectRead):
    provider: ProviderRead


class QuotaReadExtended(QuotaRead):
    project: ProjectReadExtended


class ProjectReadExtendedPublic(ProjectReadPublic):
    provider: ProviderReadPublic


class QuotaReadExtendedPublic(QuotaReadPublic):
    project: ProjectReadExtendedPublic


class ComputeQuotaReadExtended(ComputeQuotaRead, QuotaReadExtended):
    service: ComputeServiceRead


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic, QuotaReadExtendedPublic):
    service: ComputeServiceReadPublic


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead, QuotaReadExtended):
    service: BlockStorageServiceRead


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic, QuotaReadExtendedPublic):
    service: BlockStorageServiceReadPublic
