from datetime import date
from typing import Optional
from uuid import UUID

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import Field, validator


class SLABase(BaseNode):
    """Model with SLA basic attributes."""

    start_date: date = Field(description="Starting date of validity for this SLA.")
    end_date: date = Field(
        description="End of life date for this SLA. \
            If not set it lasts forever.",
    )
    doc_uuid: str = Field(description="UUID of the corresponding document.")

    @validator("doc_uuid", pre=True)
    def to_string(cls, v):
        if isinstance(v, UUID):
            return v.hex
        return v


class SLACreate(BaseNodeCreate, SLABase):
    """Model to create an SLA.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class SLAUpdate(BaseNodeCreate, SLABase):
    """Model to update an SLA.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    start_date: Optional[date] = Field(
        default=None, description="Starting date of validity for this SLA."
    )
    end_date: Optional[date] = Field(
        default=None,
        description="End of life date for this SLA. \
            If not set it lasts forever.",
    )
    doc_uuid: Optional[str] = Field(
        default=None, description="UUID of the corresponding document."
    )


class SLARead(BaseNodeRead, SLABase):
    """Model to read SLA data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class SLAReadPublic(BaseNodeRead, SLABase):
    pass


class SLAReadShort(BaseNodeRead, SLABase):
    pass


SLAQuery = create_query_model("SLAQuery", SLABase)
