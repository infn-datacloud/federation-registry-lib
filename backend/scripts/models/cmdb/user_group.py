from app.user_group.schemas import UserGroupCreate, UserGroupQuery, UserGroupRead
from pydantic import AnyHttpUrl, BaseModel


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.name}"


class UserGroupWrite(UserGroupCreate, Representation):
    identity_provider: AnyHttpUrl


class UserGroupRead(UserGroupRead, Representation):
    pass


class UserGroupQuery(UserGroupQuery, Representation):
    pass
