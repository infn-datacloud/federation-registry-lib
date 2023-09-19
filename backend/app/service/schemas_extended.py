from typing import List

from app.project.schemas import ProjectRead, ProjectReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
)
from app.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    KeystoneServiceRead,
    KeystoneServiceReadPublic,
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


class ComputeQuotaReadExtended(ComputeQuotaRead, ExtendWithProject):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""


class ComputeQuotaReadExtendedPublic(ComputeQuotaReadPublic, ExtendWithProjectPublic):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""


class BlockStorageQuotaReadExtended(BlockStorageQuotaRead, ExtendWithProject):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""


class BlockStorageQuotaReadExtendedPublic(BlockStorageQuotaReadPublic, ExtendWithProjectPublic):
    """Model to extend the Num CPUs Quota data read from the DB with the lists
    of related items."""


class ComputeServiceReadExtended(ComputeServiceRead, ExtendWithProvider):
    """Model to extend the Compute Service data read from the DB with the lists
    of related items for authenticated users."""

    quotas: List[ComputeQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas.",
    )


class ComputeServiceReadExtendedPublic(ComputeServiceReadPublic, ExtendWithProviderPublic):
    """Model to extend the Compute Service data read from the DB with the lists
    of related items for non-authenticated users."""

    quotas: List[ComputeQuotaReadExtendedPublic] = Field(
        default_factory=list,
        description="List of quotas.",
    )


class BlockStorageServiceReadExtended(BlockStorageServiceRead, ExtendWithProvider):
    """Model to extend the BlockStorage Service data read from the DB with the
    lists of related items for authenticated users."""

    quotas: List[BlockStorageQuotaReadExtended] = Field(
        default_factory=list,
        description="List of quotas.",
    )


class BlockStorageServiceReadExtendedPublic(
    BlockStorageServiceReadPublic, ExtendWithProviderPublic
):
    """Model to extend the BlockStorage Service data read from the DB with the
    lists of related items for non-authenticated users."""

    quotas: List[BlockStorageQuotaReadExtendedPublic] = Field(
        default_factory=list,
        description="List of quotas.",
    )


class KeystoneServiceReadExtended(KeystoneServiceRead, ExtendWithProvider):
    """Model to extend the Keystone Service data read from the DB with the
    lists of related items for authenticated users."""


class KeystoneServiceReadExtendedPublic(
    KeystoneServiceReadPublic, ExtendWithProviderPublic
):
    """Model to extend the Keystone Service data read from the DB with the
    lists of related items for non-authenticated users."""
