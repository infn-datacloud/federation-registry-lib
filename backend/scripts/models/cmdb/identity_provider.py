from typing import List

from app.identity_provider.schemas import IdentityProviderQuery
from app.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    IdentityProviderReadExtended,
)
from models.cmdb.user_group import UserGroupWrite
from pydantic import Field


class IdentityProviderWrite(IdentityProviderCreateExtended):
    endpoint: str = Field(alias="_id")
    user_groups: List[UserGroupWrite] = Field(
        default_factory=list, description="List of user groups"
    )

    class Config:
        allow_population_by_field_name = True


class IdentityProviderRead(IdentityProviderReadExtended):
    ...


class IdentityProviderQuery(IdentityProviderQuery):
    ...
