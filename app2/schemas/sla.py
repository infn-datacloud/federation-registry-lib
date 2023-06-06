from datetime import datetime
from typing import List, Union
from uuid import UUID
from pydantic import BaseModel, Field, validator
from neo4j.time import DateTime

from .quota import Quota
from .service import Service


def cast_neo4j_datetime(v: DateTime) -> datetime:
    if type(v) is DateTime:
        return v.to_native()
    return v


class SLABase(BaseModel):
    """Service Level Agreement (SLA) Base class

    Class expected as input when performing a REST request.
    It contains the SLA attributes

    Attributes:
        name (str): SLA name.
    """

    name: str
    start_date: datetime
    end_date: datetime
    issue_date: datetime
    # services: List[Service] = Field(default_factory=list)
    # quotas: List[Quota] = Field(default_factory=list)

    _cast_start_date = validator("start_date", pre=True, allow_reuse=True)(
        cast_neo4j_datetime
    )
    _cast_end_date = validator("end_date", pre=True, allow_reuse=True)(
        cast_neo4j_datetime
    )
    _cast_issue_date = validator("issue_date", pre=True, allow_reuse=True)(
        cast_neo4j_datetime
    )

    class Config:
        validate_assignment = True


class SLACreate(SLABase):
    """Service Level Agreement (SLA) Actors class

    Class expected as input when performing a REST request.
    It contains the SLA actors.

    Attributes:
        project_id (int): ID of the target Project.
        provider_id (int): ID of the target Provider.
        service_id (int): ID of the target Resource.
    """

    pass


class SLA(SLABase):
    """Service Level Agreement (SLA) Base class

    Class expected as output when performing a REST request.
    It contains all the non-sensible data written in the database.

    Attributes:
        id (str): SLA unique ID.
        name (str): SLA name.
        project_id (int): ID of the target Project.
        provider_id (int): ID of the target Provider.
        service_id (int): ID of the target Resource.
    """

    id: UUID
    project_id: UUID
    provider_id: UUID

    class Config:
        orm_mode = True
