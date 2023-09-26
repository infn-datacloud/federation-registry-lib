from typing import List

from app.sla.schemas import SLACreate, SLAQuery, SLARead
from pydantic import UUID4, Field


class SLAWrite(SLACreate):
    doc_uuid: UUID4 = Field(alias="_id")
    projects: List[UUID4] = Field(
        default_factory=list, description="List of project UUID"
    )

    class Config:
        allow_population_by_field_name = True


class SLARead(SLARead):
    pass


class SLAQuery(SLAQuery):
    pass
