from typing import Optional

from app.quota.schemas import (
    CinderQuotaCreate,
    NovaQuotaCreate,
    QuotaCreate,
    QuotaQuery,
    QuotaRead,
)
from pydantic import UUID4, Field


class QuotaWrite(QuotaCreate):
    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.type}"


class NovaQuotaWrite(NovaQuotaCreate):
    type: str = "org.openstack.nova"
    service: Optional[UUID4] = Field(default=None, description="")

    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.type}"


class CinderQuotaWrite(CinderQuotaCreate):
    type: str = "org.openstack.cinder"
    service: Optional[UUID4] = Field(default=None, description="")

    def __str__(self) -> str:
        return f"{self.__class__.__name__.replace('Write', '')}={self.type}"


class QuotaRead(QuotaRead):
    pass


class QuotaQuery(QuotaQuery):
    pass
