from typing import Optional

from app.quota.schemas import (
    CinderQuotaCreate,
    NovaQuotaCreate,
    QuotaCreate,
    QuotaQuery,
    QuotaRead,
)
from pydantic import UUID4, BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.type}"


class QuotaWrite(QuotaCreate, Representation):
    pass


class NovaQuotaWrite(NovaQuotaCreate, Representation):
    type: str = "org.openstack.nova"
    service: Optional[UUID4] = Field(default=None, description="")


class CinderQuotaWrite(CinderQuotaCreate, Representation):
    type: str = "org.openstack.cinder"
    service: Optional[UUID4] = Field(default=None, description="")


class QuotaRead(QuotaRead, Representation):
    pass


class QuotaQuery(QuotaQuery, Representation):
    pass
