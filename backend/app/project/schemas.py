from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import UUID4, BaseModel, Field


class ProjectBase(BaseModel):
    """Model with Project basic attributes."""

    name: str = Field(description="Project name in the provider.")
    uuid: UUID4 = Field(description="Project UUID in the provider.")
    public_network_name: Optional[str] = Field(
        default=None, description=""
    )  # TODO
    private_network_name: Optional[str] = Field(
        default=None, description=""
    )  # TODO
    private_network_proxy_host: Optional[str] = Field(
        default=None, description=""
    )  # TODO
    private_network_proxy_user: Optional[str] = Field(
        default=None, description=""
    )  # TODO


class ProjectCreate(BaseNodeCreate, ProjectBase):
    """Model to create a Project.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.
    """


class ProjectUpdate(ProjectCreate):
    """Model to update a Project.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

    Default to None mandatory attributes.
    """

    name: Optional[str] = Field(
        default=None, description="Project name in the provider."
    )
    uuid: Optional[UUID4] = Field(
        default=None, description="Project UUID in the provider."
    )


class ProjectRead(BaseNodeRead, ProjectBase):
    """Model to read Project data retrieved from DB.

    Class to read data retrieved from the database.
    Expected as output when performing a generic REST request.
    It contains all the non-sensible data written in the database.

    Add the *uid* attribute, which is the item unique
    identifier in the database.
    """


ProjectQuery = create_query_model("ProjectQuery", ProjectBase)
