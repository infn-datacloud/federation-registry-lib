"""Pydantic models of the User Group owned by an Identity Provider."""

from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, Field

from fedreg.core import BaseNode, BaseNodeRead, PaginationQuery


class UserGroupBase(BaseNode):
    """Base schema for a user group in the Identity Provider.

    Attributes:
        name (str): User group name in the Identity Provider.
    """

    name: Annotated[str, Field(description="User group name in the Identity Provider.")]


class UserGroupCreate(UserGroupBase):
    """Schema for creating a new user group.

    Inherits all fields from UserGroupBase.
    """


class UserGroupLinks(BaseModel):
    """Schema representing hyperlinks related to a user group.

    Attributes:
        projects (AnyHttpUrl): Link to the user group's projects endpoint.
    """

    projects: Annotated[
        AnyHttpUrl, Field(description="Link to the user group's projects endpoint.")
    ]


class UserGroupRead(BaseNodeRead, UserGroupBase):
    """Represents a user group with associated project IDs and related hyperlinks.

    Inherits from:
        BaseNodeRead: Base class for node read operations.
        UserGroupBase: Base class for user group attributes.

    Attributes:
        projects (list[str]): List of project IDs associated with the user group.
        links (UserGroupLinks): Hyperlinks related to the user group.
    """

    projects: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of project IDs associated with the user group.",
        ),
    ]
    links: Annotated[
        UserGroupLinks, Field(description="Hyperlinks related to the user group.")
    ]


class UserGroupQuery(PaginationQuery):
    """Schema for querying user groups.

    Inherits from BaseNode to include common node attributes.
    This schema is used for filtering and retrieving user group data.
    """

    name: Annotated[
        str | None,
        Field(default=None, description="User group name in the Identity Provider."),
    ]
