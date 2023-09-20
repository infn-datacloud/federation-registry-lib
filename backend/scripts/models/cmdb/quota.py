from app.quota.schemas import (
    BlockStorageQuotaCreate,
    ComputeQuotaCreate,
    QuotaCreate,
    QuotaQuery,
    QuotaRead,
)
from app.service.enum import ServiceType
from pydantic import AnyHttpUrl, BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.type}"


class QuotaWrite(QuotaCreate, Representation):
    pass


class ComputeQuotaWrite(ComputeQuotaCreate, Representation):
    type: ServiceType = Field(default=ServiceType.COMPUTE)
    service: AnyHttpUrl = Field(default=None, description="")


class BlockStorageQuotaWrite(BlockStorageQuotaCreate, Representation):
    type: ServiceType = Field(default=ServiceType.BLOCK_STORAGE)
    service: AnyHttpUrl = Field(default=None, description="")


class QuotaRead(QuotaRead, Representation):
    pass


class QuotaQuery(QuotaQuery, Representation):
    pass