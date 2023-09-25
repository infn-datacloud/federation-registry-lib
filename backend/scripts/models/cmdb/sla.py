from app.sla.schemas import SLACreate, SLAQuery, SLARead
from pydantic import UUID4, Field


class SLAWrite(SLACreate):
    doc_uuid: UUID4 = Field(alias="_id")
    project: UUID4 = Field(description="Project UUID")

    class Config:
        allow_population_by_field_name = True


class SLARead(SLARead):
    pass


class SLAQuery(SLAQuery):
    pass
