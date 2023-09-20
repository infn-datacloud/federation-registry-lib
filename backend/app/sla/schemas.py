from datetime import date

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import UUID4, Field


class SLABase(BaseNode):
    """Model with SLA basic attributes."""

    start_date: date = Field(description="Starting date of validity for this SLA.")
    end_date: date = Field(
        description="End of life date for this SLA. \
            If not set it lasts forever.",
    )
    doc_uuid: UUID4 = Field(description="UUID of the corresponding document.")


class SLACreate(BaseNodeCreate, SLABase):
    """Model to create an SLA.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class SLAUpdate(SLACreate):
    """Model to update an SLA.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """


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
