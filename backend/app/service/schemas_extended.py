from typing import List

from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import NovaQuotaRead, NovaQuotaReadPublic
from app.service.schemas import (
    CinderServiceRead,
    CinderServiceReadPublic,
    KeystoneServiceRead,
    KeystoneServiceReadPublic,
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


class NovaQuotaReadExtended(NovaQuotaRead, ExtendWithProject):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""


class NovaQuotaReadExtendedPublic(NovaQuotaReadPublic, ExtendWithProjectPublic):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""


class NovaServiceReadExtended(NovaServiceRead, ExtendWithProvider):
    """Model to extend the Nova Service data read from the DB with the lists of
    related items for authenticated users."""

    quotas: List[NovaQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas.",
    )


class NovaServiceReadExtendedPublic(NovaServiceReadPublic, ExtendWithProviderPublic):
    """Model to extend the Nova Service data read from the DB with the lists of
    related items for non-authenticated users."""

    quotas: List[NovaQuotaReadExtendedPublic] = Field(
        default_factory=list,
        description="List of quotas.",
    )


class CinderServiceReadExtended(CinderServiceRead, ExtendWithProvider):
    """Model to extend the Cinder Service data read from the DB with the lists
    of related items for authenticated users."""


class CinderServiceReadExtendedPublic(
    CinderServiceReadPublic, ExtendWithProviderPublic
):
    """Model to extend the Cinder Service data read from the DB with the lists
    of related items for non-authenticated users."""


class KeystoneServiceReadExtended(KeystoneServiceRead, ExtendWithProvider):
    """Model to extend the Keystone Service data read from the DB with the
    lists of related items for authenticated users."""


class KeystoneServiceReadExtendedPublic(
    KeystoneServiceReadPublic, ExtendWithProviderPublic
):
    """Model to extend the Keystone Service data read from the DB with the
    lists of related items for non-authenticated users."""
