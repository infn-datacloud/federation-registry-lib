from typing import List

from app.provider.schemas_extended import UserGroupReadExtended
from app.user_group.schemas import UserGroupCreate, UserGroupQuery
from models.cmdb.sla import SLAWrite
from pydantic import Field


class UserGroupWrite(UserGroupCreate):
    name: str = Field(alias="_id")
    slas: List[SLAWrite] = Field(
        default_factory=list, description="List of registered SLAs"
    )

    class Config:
        allow_population_by_field_name = True


class UserGroupRead(UserGroupReadExtended):
    ...


class UserGroupQuery(UserGroupQuery):
    ...
