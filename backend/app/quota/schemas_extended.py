from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    CinderQuotaRead,
    CinderQuotaReadPublic,
    NovaQuotaRead,
    NovaQuotaReadPublic,
    QuotaRead,
    QuotaReadPublic,
)
from app.service.schemas import (
    CinderServiceRead,
    CinderServiceReadPublic,
    NovaServiceRead,
    NovaServiceReadPublic,
)


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


class CinderQuotaReadExtended(CinderQuotaRead, QuotaReadExtended):
    service: CinderServiceRead


class CinderQuotaReadExtendedPublic(CinderQuotaReadPublic, QuotaReadExtendedPublic):
    service: CinderServiceReadPublic
