from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import BaseModel, Field


class UserGroupBase(BaseModel):
    """Model with User Group basic attributes."""

    name: str = Field(description="User group name.")


class UserGroupCreate(BaseNodeCreate, UserGroupBase):
    """Model to create a User Group.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.

    Validation: If *num GPUs* is 0, then *gpu model*
    and *gpu vendor* must be none.
    """


class UserGroupUpdate(UserGroupCreate):
    """Model to update a User Group.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

    Default to None mandatory attributes.
    """

    name: Optional[str] = Field(default=None, description="User group name.")


class UserGroupRead(BaseNodeRead, UserGroupBase):
    """Model to read User Group data retrieved from DB.

    Class to read data retrieved from the database.
    Expected as output when performing a generic REST request.
    It contains all the non-sensible data written in the database.

    Add the *uid* attribute, which is the item unique
    identifier in the database.
    """


UserGroupQuery = create_query_model("UserGroupQuery", UserGroupBase)
