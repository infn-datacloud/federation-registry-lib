from typing import List

from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    NumCPUQuotaRead,
    NumCPUQuotaReadPublic,
    RAMQuotaRead,
    RAMQuotaReadPublic,
)
from app.service.schemas import (
    KubernetesServiceRead,
    KubernetesServiceReadPublic,
    NovaServiceRead,
    NovaServiceReadPublic,
)
from pydantic import BaseModel, Field


class ExtendWithProvider(BaseModel):
    """Model to extend a Service with the hosting provider."""

    provider: ProviderRead


class ExtendWithProject(BaseModel):
    """Model to extend a Quota with the project owning it."""

    project: ProjectRead


class ExtendWithProviderPublic(BaseModel):
    """Model to extend a Service with the hosting provider."""

    provider: ProviderReadPublic


class ExtendWithProjectPublic(BaseModel):
    """Model to extend a Quota with the project owning it."""

    project: ProjectReadPublic


class NumCPUQuotaReadExtended(NumCPUQuotaRead, ExtendWithProject):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""


class RAMQuotaReadExtended(RAMQuotaRead, ExtendWithProject):
    """Model to extend the RAM Quota data read from the DB with the lists of
    related items."""


class NumCPUQuotaReadExtendedPublic(NumCPUQuotaReadPublic, ExtendWithProjectPublic):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""


class RAMQuotaReadExtendedPublic(RAMQuotaReadPublic, ExtendWithProjectPublic):
    """Model to extend the RAM Quota data read from the DB with the lists of
    related items."""


class NovaServiceReadExtended(NovaServiceRead, ExtendWithProvider):
    """Model to extend the Nova Service data read from the DB with the lists of
    related items for authenticated users."""

    num_cpu_quotas: List[NumCPUQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas related to the CPUs number usage.",
    )
    ram_quotas: List[RAMQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas related to the RAM usage.",
    )


class NovaServiceReadExtendedPublic(NovaServiceReadPublic, ExtendWithProviderPublic):
    """Model to extend the Nova Service data read from the DB with the lists of
    related items for non-authenticated users."""

    num_cpu_quotas: List[NumCPUQuotaReadExtendedPublic] = Field(
        default_factory=list,
        description="List of quotas related to the CPUs number usage.",
    )
    ram_quotas: List[RAMQuotaReadExtendedPublic] = Field(
        default_factory=list,
        description="List of quotas related to the RAM usage.",
    )


class KubernetesServiceReadExtended(KubernetesServiceRead, ExtendWithProvider):
    """Model to extend the Nova Service data read from the DB with the lists of
    related items for authenticated users."""

    num_cpu_quotas: List[NumCPUQuotaReadExtended] = Field(default_factory=list)
    ram_quotas: List[RAMQuotaReadExtended] = Field(default_factory=list)


class KubernetesServiceReadExtendedPublic(
    KubernetesServiceReadPublic, ExtendWithProviderPublic
):
    """Model to extend the Nova Service data read from the DB with the lists of
    related items for non-authenticated users."""

    num_cpu_quotas: List[NumCPUQuotaReadExtendedPublic] = Field(default_factory=list)
    ram_quotas: List[RAMQuotaReadExtendedPublic] = Field(default_factory=list)
