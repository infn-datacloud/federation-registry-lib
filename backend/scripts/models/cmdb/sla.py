from app.sla.schemas import SLACreate, SLAQuery, SLARead
from models.cmdb.user_group import UserGroupWrite
from pydantic import BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.doc_uuid}"


class SLAWrite(SLACreate, Representation):
    user_group: UserGroupWrite = Field(
        description="List of user groups having access to this SLA",
    )


class SLARead(SLARead, Representation):
    pass


class SLAQuery(SLAQuery, Representation):
    pass
