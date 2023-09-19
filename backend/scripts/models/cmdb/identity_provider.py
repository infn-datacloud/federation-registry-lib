from typing import List

from app.identity_provider.schemas import IdentityProviderQuery
from app.identity_provider.schemas_extended import IdentityProviderReadExtended
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
)
from app.user_group.schemas import UserGroupRead
from pydantic import BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.endpoint}"


class IdentityProviderWrite(IdentityProviderCreateExtended, Representation):
    pass


class IdentityProviderRead(IdentityProviderReadExtended, Representation):
    user_groups: List[UserGroupRead] = Field(default_factory=list)


class IdentityProviderQuery(IdentityProviderQuery, Representation):
    pass


class AuthMethodWrite(AuthMethodCreate):
    pass
