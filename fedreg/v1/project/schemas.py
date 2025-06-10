"""Pydantic models of the Project owned by a Provider."""

from pydantic.v1 import Field

from fedreg.v1.core import (
    BaseNode,
    BaseNodeCreate,
    BaseNodeRead,
    BaseReadPrivate,
    BaseReadPublic,
    create_query_model,
)
from fedreg.v1.project.constants import DOC_NAME, DOC_UUID


class ProjectBasePublic(BaseNode):
    """Model with Project public attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Project name in the Provider.
        uuid (str): Project unique ID in the Provider
    """

    name: str = Field(description=DOC_NAME)
    uuid: str = Field(description=DOC_UUID)


class ProjectBase(ProjectBasePublic):
    """Model with Project public and restricted attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Project name in the Provider.
        uuid (str): Project unique ID in the Provider
    """


class ProjectCreate(BaseNodeCreate, ProjectBase):
    """Model to create a Project.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Project name in the Provider.
        uuid (str): Project unique ID in the Provider
    """


class ProjectUpdate(BaseNodeCreate, ProjectBase):
    """Model to update a Project.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): Project name in the Provider.
        uuid (str | None): Project unique ID in the Provider
    """

    name: str | None = Field(default=None, description=DOC_NAME)
    uuid: str | None = Field(default=None, description=DOC_UUID)


class ProjectReadPublic(BaseNodeRead, BaseReadPublic, ProjectBasePublic):
    """Model, for non-authenticated users, to read Project data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Project unique ID.
        description (str): Brief description.
        name (str): Project name in the Provider.
        uuid (str): Project unique ID in the Provider
    """


class ProjectRead(BaseNodeRead, BaseReadPrivate, ProjectBase):
    """Model, for authenticated users, to read Project data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Project name in the Provider.
        uuid (str): Project unique ID in the Provider
    """


ProjectQuery = create_query_model("ProjectQuery", ProjectBase)
