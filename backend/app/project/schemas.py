from typing import Optional
from uuid import UUID

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import Field, validator


class ProjectBase(BaseNode):
    """Model with Project basic attributes."""

    name: str = Field(description="Project name in the provider.")
    uuid: str = Field(description="Project UUID in the provider.")

    @validator("uuid", pre=True)
    def to_string(cls, v):
        if isinstance(v, UUID):
            return v.hex
        return v


class ProjectCreate(BaseNodeCreate, ProjectBase):
    """Model to create a Project.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class ProjectUpdate(ProjectCreate):
    """Model to update a Project.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    name: Optional[str] = Field(
        default=None, description="Project name in the provider."
    )
    uuid: Optional[str] = Field(
        default=None, description="Project UUID in the provider."
    )


class ProjectRead(BaseNodeRead, ProjectBase):
    """Model to read Project data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class ProjectReadPublic(BaseNodeRead, ProjectBase):
    pass


class ProjectReadShort(BaseNodeRead, ProjectBase):
    pass


ProjectQuery = create_query_model("ProjectQuery", ProjectBase)
