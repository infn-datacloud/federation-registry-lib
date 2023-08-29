from typing import Union

from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.quota.schemas import NumCPUQuotaRead, QuotaRead, RAMQuotaRead
from app.service.schemas import (
    ChronosServiceRead,
    KubernetesServiceRead,
    MarathonServiceRead,
    MesosServiceRead,
    NovaServiceRead,
    OneDataServiceRead,
    RucioServiceRead,
)


class ProjectReadExtended(ProjectRead):
    provider: ProviderRead


class QuotaReadExtended(QuotaRead):
    project: ProjectReadExtended
    service: Union[
        ChronosServiceRead,
        KubernetesServiceRead,
        MarathonServiceRead,
        MesosServiceRead,
        NovaServiceRead,
        OneDataServiceRead,
        RucioServiceRead,
    ]


class NumCPUQuotaReadExtended(NumCPUQuotaRead, QuotaReadExtended):
    pass


class RAMQuotaReadExtended(RAMQuotaRead, QuotaReadExtended):
    pass
