from app.sla.schemas import SLACreate, SLAQuery, SLARead
from pydantic import UUID4, BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.doc_uuid}"


class SLAWrite(SLACreate, Representation):
    project: UUID4 = Field(description="Project UUID")


class SLARead(SLARead, Representation):
    pass


class SLAQuery(SLAQuery, Representation):
    pass
