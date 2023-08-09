from datetime import datetime
from pydantic import UUID4, BaseModel, Field
from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class SLABase(BaseModel):
    """Model with SLA basic attributes."""

    start_date: datetime = Field(
        description="Starting date of validity for this SLA."
    )
    end_date: Optional[datetime] = Field(
        default=None,
        description="End of life date for this SLA. \
            If not set it lasts forever.",
    )
    document_uuid: Optional[UUID4] = Field(
        default=None, description="UUID of the corresponding document."
    )


class SLACreate(BaseNodeCreate, SLABase):
    """Model to create an SLA.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.
    """


class SLAUpdate(SLACreate):
    """Model to update an SLA.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

    Default to None mandatory attributes.
    """
    start_date: Optional[datetime] = Field(
        default=None, description="Starting date of validity for this SLA."
    )


class SLARead(BaseNodeRead, SLABase):
    """Model to read SLA data retrieved from DB.

    Class to read data retrieved from the database.
    Expected as output when performing a generic REST request.
    It contains all the non-sensible data written in the database.

    Add the *uid* attribute, which is the item unique
    identifier in the database.
    """


SLAQuery = create_query_model("SLAQuery", SLABase)
