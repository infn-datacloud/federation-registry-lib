from app.quota.schemas import (
    BlockStorageQuotaBase,
    BlockStorageQuotaCreate,
    BlockStorageQuotaQuery,
    ComputeQuotaBase,
    ComputeQuotaCreate,
    ComputeQuotaQuery,
)
from app.service.enum import ServiceType
from pydantic import UUID4, AnyHttpUrl, Field


class ComputeQuotaWrite(ComputeQuotaCreate):
    type: ServiceType = Field(default=ServiceType.COMPUTE, alias="_id")
    service: AnyHttpUrl = Field(default=None, description="")
    project: UUID4 = Field(description="Project UUID")

    class Config:
        allow_population_by_field_name = True


class BlockStorageQuotaWrite(BlockStorageQuotaCreate):
    type: ServiceType = Field(default=ServiceType.BLOCK_STORAGE, alias="_id")
    service: AnyHttpUrl = Field(default=None, description="")
    project: UUID4 = Field(description="Project UUID")

    class Config:
        allow_population_by_field_name = True


class BlockStorageQuotaRead(BlockStorageQuotaBase):
    ...


class BlockStorageQuotaQuery(BlockStorageQuotaQuery):
    ...


class ComputeQuotaRead(ComputeQuotaBase):
    ...


class ComputeQuotaQuery(ComputeQuotaQuery):
    ...
