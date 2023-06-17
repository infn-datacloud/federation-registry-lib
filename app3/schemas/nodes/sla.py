from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from uuid import UUID

from .project import Project
from .service import Service
from .user_group import UserGroup
from ..relationships import Quota, QuotaCreate
from ..utils import cast_neo4j_datetime


class SLAServiceCreate(BaseModel):
    uid: UUID
    relationships: List[QuotaCreate]

    class Config:
        validate_assignment = True


class SLAService(Service):
    relationships: List[Quota]


class SLABase(BaseModel):
    """Service Level Agreement (SLA) Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        validate_assignment = True


class SLAUpdate(SLABase):
    """Service Level Agreement (SLA) Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    description: str = ""
    project: Optional[UUID] = None
    user_group: Optional[UUID] = None
    services: List[SLAServiceCreate] = Field(default_factory=list)


class SLACreate(SLAUpdate):
    """Service Level Agreement (SLA) Actors class

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    start_date: datetime
    end_date: datetime
    project: UUID
    user_group: UUID
    services: List[SLAServiceCreate]


class SLA(SLACreate):
    """Service Level Agreement (SLA) Base class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): SLA unique ID.
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    uid: UUID
    project: Project
    user_group: UserGroup
    services: List[SLAService]

    _cast_start_date = validator("start_date", pre=True, allow_reuse=True)(
        cast_neo4j_datetime
    )
    _cast_end_date = validator("end_date", pre=True, allow_reuse=True)(
        cast_neo4j_datetime
    )

    @validator("project", pre=True)
    def get_single_project(cls, v):
        return v.single()

    @validator("user_group", pre=True)
    def get_single_user_group(cls, v):
        return v.single()

    @validator("services", pre=True)
    def get_all_services(cls, v):
        services = []
        for node in v.all():
            services.append(
                SLAService(
                    **node.__dict__, relationships=v.all_relationships(node)
                )
            )
        return services

    class Config:
        orm_mode = True
