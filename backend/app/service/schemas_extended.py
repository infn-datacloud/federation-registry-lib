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
from pydantic import BaseModel, Field


class ExtendWithProvider(BaseModel):
    """Model to extend a Service with the hosting provider."""

    provider: ProviderRead


class ExtendWithProject(BaseModel):
    """Model to extend a Quota with the project owning it."""

    project: ProjectRead


class NumCPUQuotaReadExtended(NumCPUQuotaRead, ExtendWithProject):
    """Model to extend the Num CPUs Quota data read from the
    DB with the lists of related items.
    """


class RAMQuotaReadExtended(RAMQuotaRead, ExtendWithProject):
    """Model to extend the RAM Quota data read from the
    DB with the lists of related items.
    """


class NovaServiceReadExtended(NovaServiceRead, ExtendWithProvider):
    """Model to extend the Nova Service data read from the
    DB with the lists of related items.
    """

    num_cpu_quotas: List[NumCPUQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas related to the CPUs number usage.",
    )
    ram_quotas: List[RAMQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas related to the RAM usage.",
    )


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
