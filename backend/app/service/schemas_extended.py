from pydantic import BaseModel, Field
from typing import List

from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.quota.schemas import NumCPUQuotaRead, RAMQuotaRead
from app.service.schemas import (
    ChronosServiceRead,
    KubernetesServiceRead,
    MarathonServiceRead,
    MesosServiceRead,
    NovaServiceRead,
    OneDataServiceRead,
    RucioServiceRead,
)


class ExtendWithProvider(BaseModel):
    provider: ProviderRead


class ExtendWithProject(BaseModel):
    project: ProjectRead


class NumCPUQuotaReadExtended(NumCPUQuotaRead, ExtendWithProject):
    pass


class RAMQuotaReadExtended(RAMQuotaRead, ExtendWithProject):
    pass


class NovaServiceReadExtended(NovaServiceRead, ExtendWithProvider):
    num_cpu_quotas: List[NumCPUQuotaReadExtended] = Field(default_factory=list)
    ram_quotas: List[RAMQuotaReadExtended] = Field(default_factory=list)


class MesosServiceReadExtended(MesosServiceRead, ExtendWithProvider):
    pass


class ChronosServiceReadExtended(ChronosServiceRead, ExtendWithProvider):
    pass


class MarathonServiceReadExtended(MarathonServiceRead, ExtendWithProvider):
    pass


class KubernetesServiceReadExtended(KubernetesServiceRead, ExtendWithProvider):
    num_cpu_quotas: List[NumCPUQuotaReadExtended] = Field(default_factory=list)
    ram_quotas: List[RAMQuotaReadExtended] = Field(default_factory=list)


class RucioServiceReadExtended(RucioServiceRead, ExtendWithProvider):
    pass


class OneDataServiceReadExtended(OneDataServiceRead, ExtendWithProvider):
    pass
