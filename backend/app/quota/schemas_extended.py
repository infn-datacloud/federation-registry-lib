from typing import Union

from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.quota.schemas import NumCPUQuotaRead, QuotaRead, RAMQuotaRead
from app.service.schemas import CinderServiceRead, KeystoneServiceRead, NovaServiceRead


class ProjectReadExtended(ProjectRead):
    provider: ProviderRead


class QuotaReadExtended(QuotaRead):
    project: ProjectReadExtended
    service: Union[
        CinderServiceRead,
        KeystoneServiceRead,
        NovaServiceRead,
    ]


class NumCPUQuotaReadExtended(NumCPUQuotaRead, QuotaReadExtended):
    pass


class RAMQuotaReadExtended(RAMQuotaRead, QuotaReadExtended):
    pass
