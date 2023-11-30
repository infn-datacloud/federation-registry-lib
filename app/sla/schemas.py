"""Service Level Agreement between a Project and a User Group pydantic models."""
from datetime import date
from typing import Any, Dict, Optional

from pydantic import Field, root_validator

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class SLABase(BaseNode):
    """Model with SLA basic attributes.

    Attributes:
    ----------
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    start_date: date = Field(description="Starting date of validity for this SLA.")
    end_date: date = Field(
        description="End of life date for this SLA. \
            If not set it lasts forever.",
    )
    doc_uuid: str = Field(description="UUID of the corresponding document.")


class SLACreate(BaseNodeCreate, SLABase):
    """Model to create an SLA.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """

    @root_validator
    def start_date_before_end_date(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Verify start date precedes end date."""
        start = values.get("start_date")
        end = values.get("end_date")
        assert start < end, f"Start date {start} greater than end date {end}"
        return values


class SLAUpdate(BaseNodeCreate, SLABase):
    """Model to update an SLA.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        doc_uuid (str | None): Unique ID of the document with the SLA details.
        start_date (datetime | None): SLA validity start date.
        end_date (datetime | None): SLA validity end date.
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

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): SLA unique ID.
        description (str): Brief description.
        doc_uuid (str): Unique ID of the document with the SLA details.
        start_date (datetime): SLA validity start date.
        end_date (datetime): SLA validity end date.
    """


class SLAReadPublic(BaseNodeRead, SLABase):
    pass


class SLAReadShort(BaseNodeRead, SLABase):
    pass


SLAQuery = create_query_model("SLAQuery", SLABase)
