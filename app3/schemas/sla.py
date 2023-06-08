from datetime import datetime
from neo4j.time import DateTime
from pydantic import BaseModel, validator


def cast_neo4j_datetime(v: DateTime) -> datetime:
    """Convert neo4j datetime to datetime"""
    if type(v) is DateTime:
        return v.to_native()
    return v


class SLABase(BaseModel):
    """Service Level Agreement (SLA) Base class

    Class without id (which is populated by the database).

    Attributes:
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    description: str = ""
    start_date: datetime
    end_date: datetime

    _cast_start_date = validator("start_date", pre=True, allow_reuse=True)(
        cast_neo4j_datetime
    )
    _cast_end_date = validator("end_date", pre=True, allow_reuse=True)(
        cast_neo4j_datetime
    )

    class Config:
        validate_assignment = True


class SLACreate(SLABase):
    """Service Level Agreement (SLA) Actors class

    Class without id (which is populated by the database).
    expected as input when performing a REST request.

    Attributes:
        description (str): Brief description.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    pass


class SLA(SLABase):
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

    uid: str

    class Config:
        orm_mode = True
