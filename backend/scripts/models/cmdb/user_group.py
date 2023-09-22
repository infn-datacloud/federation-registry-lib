from app.sla.schemas import SLACreate
from app.user_group.schemas import UserGroupCreate, UserGroupQuery, UserGroupRead
from pydantic import BaseModel


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.name}"


class UserGroupWrite(UserGroupCreate, Representation):
    sla: SLACreate


class UserGroupRead(UserGroupRead, Representation):
    pass


class UserGroupQuery(UserGroupQuery, Representation):
    pass
