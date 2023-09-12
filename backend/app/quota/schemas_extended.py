from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    NovaQuotaRead,
    NovaQuotaReadPublic,
    QuotaRead,
    QuotaReadPublic,
)
from app.service.schemas import NovaServiceRead, NovaServiceReadPublic


class ProjectReadExtended(ProjectRead):
    provider: ProviderRead


class QuotaReadExtended(QuotaRead):
    project: ProjectReadExtended


class ProjectReadExtendedPublic(ProjectReadPublic):
    provider: ProviderReadPublic


class QuotaReadExtendedPublic(QuotaReadPublic):
    project: ProjectReadExtendedPublic


class NovaQuotaReadExtended(NovaQuotaRead, QuotaReadExtended):
    service: NovaServiceRead


class NovaQuotaReadExtendedPublic(NovaQuotaReadPublic, QuotaReadExtendedPublic):
    service: NovaServiceReadPublic
