"""Pydantic models of the Project owned by a Provider."""

from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, Field

from fedreg.core import BaseNode, BaseNodeRead


class ProjectBase(BaseNode):
    """Model with Project attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Project name in the Provider.
        uuid (str): Project unique ID in the Provider
    """

    name: Annotated[str, Field(description="Project friendly name.")]
    uuid: Annotated[str, Field(description="Project unique ID in the Provider.")]


class ProjectCreate(ProjectBase):
    """Model to create a Project.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Project name in the Provider.
        uuid (str): Project unique ID in the Provider
    """


class ProjectLinks(BaseModel):
    quotas: Annotated[
        AnyHttpUrl, Field(description="Link to the quotas associated with the Project.")
    ]
    flavors: Annotated[
        AnyHttpUrl,
        Field(description="Link to the flavors associated with the Project."),
    ]
    images: Annotated[
        AnyHttpUrl, Field(description="Link to the images associated with the Project.")
    ]
    networks: Annotated[
        AnyHttpUrl,
        Field(description="Link to the networks associated with the Project."),
    ]


class ProjectRead(BaseNodeRead, ProjectBase):
    """Model, for non-authenticated users, to read Project data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *id* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        id (str): Project unique ID.
        description (str): Brief description.
        name (str): Project name in the Provider.
        uuid (str): Project unique ID in the Provider
    """

    quotas: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of Quotas associated with the Project.",
        ),
    ]
    flavors: Annotated[
        list[str], Field(default_factory=list, description="List of Flavors.")
    ]
    images: Annotated[
        list[str], Field(default_factory=list, description="List of Images.")
    ]
    networks: Annotated[
        list[str], Field(default_factory=list, description="List of Networks.")
    ]
    links: Annotated[ProjectLinks, Field(description="Links to the Project resources.")]


class ProjectQuery(BaseModel):
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

    name: Annotated[
        str | None, Field(default=None, description="Project friendly name.")
    ]
    uuid: Annotated[
        str | None,
        Field(default=None, description="Project unique ID in the Provider."),
    ]
