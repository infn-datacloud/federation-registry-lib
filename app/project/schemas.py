"""Project owned by a Provider pydantic models."""
from typing import Optional

from pydantic import Field

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class ProjectBase(BaseNode):
    """Model with Project basic attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
    """

    name: str = Field(description="Project name in the provider.")
    uuid: str = Field(description="Project UUID in the provider.")


class ProjectCreate(BaseNodeCreate, ProjectBase):
    """Model to create a Project.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
    """


class ProjectUpdate(BaseNodeCreate, ProjectBase):
    """Model to update a Project.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): Name of the project in the Provider.
        uuid (uuid | None): Project Unique ID in the Provider.
    """

    name: Optional[str] = Field(
        default=None, description="Project name in the provider."
    )
    uuid: Optional[str] = Field(
        default=None, description="Project UUID in the provider."
    )


class ProjectRead(BaseNodeRead, ProjectBase):
    """Model to read Project data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
    """


class ProjectReadPublic(BaseNodeRead, ProjectBase):
    pass


class ProjectReadShort(BaseNodeRead, ProjectBase):
    pass


ProjectQuery = create_query_model("ProjectQuery", ProjectBase)
