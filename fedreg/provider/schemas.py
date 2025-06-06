"""Pydantic models of the Resource Provider (openstack, kubernetes...)."""

from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, Field

from fedreg.core import BaseNode, BaseNodeRead, PaginationQuery
from fedreg.provider.enum import ProviderType


class ProviderBase(BaseNode):
    """ProviderBase represents the base schema for a provider entity.

    Attributes:
        name (str): Provider name.
        type (ProviderType): Provider type.
        is_public (bool): Indicates if the provider is public or private.
            Defaults to False.
        connection_url (AnyHttpUrl): Provider connection URL.
    """

    name: Annotated[str, Field(description="Provider name.")]
    type: Annotated[ProviderType, Field(description="Provider type.")]
    is_public: Annotated[
        bool, Field(default=False, description="Public or private Provider.")
    ]
    connection_url: Annotated[AnyHttpUrl, Field(description="Provider connection URL.")]


class ProviderCreate(ProviderBase):
    """Schema for creating a new Provider.

    Inherits all fields from ProviderBase.
    """


class ProviderLinks(BaseModel):
    """
    ProviderLinks defines the URLs to various endpoints exposed by a Provider.

    Attributes:
        regions (AnyHttpUrl): Link to the Provider's regions endpoint.
        projects (AnyHttpUrl): Link to the Provider's projects endpoint.
        idps (AnyHttpUrl): Link to the Provider's Identity Providers endpoint.
    """

    regions: Annotated[
        AnyHttpUrl, Field(description="Link to the Provider's regions endpoint.")
    ]
    projects: Annotated[
        AnyHttpUrl, Field(description="Link to the Provider's projects endpoint.")
    ]
    idps: Annotated[
        AnyHttpUrl,
        Field(description="Link to the Provider's Identity Providers endpoint."),
    ]


class ProviderRead(BaseNodeRead, ProviderBase):
    """Represents a read-only view of a Provider.

    Includes associated regions, projects, identity providers, and related hyperlinks.

    Attributes:
        regions (list[str]): List of region IDs associated with the Provider.
        projects (list[str]): List of project IDs associated with the Provider.
        idps (list[str]): List of Identity Provider IDs associated with the Provider.
        links (ProviderLinks): Hyperlinks related to the Provider.
    """

    regions: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of region IDs associated with the Provider.",
        ),
    ]
    projects: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of project IDs associated with the Provider.",
        ),
    ]
    idps: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of Identity Provider IDs associated with the Provider.",
        ),
    ]
    links: Annotated[
        ProviderLinks, Field(description="Hyperlinks related to the Provider.")
    ]


class ProviderQuery(PaginationQuery):
    """
    ProviderQuery model for querying provider entities.

    Attributes:
        name (str | None): Provider name.
        type (str | None): Provider type.
        is_public (bool | None): Indicates if the provider is public or private.
        connection_url (str | None): Provider connection URL.
    """

    name: Annotated[str | None, Field(default=None, description="Provider name.")]
    type: Annotated[str | None, Field(default=None, description="Provider type.")]
    is_public: Annotated[
        bool | None, Field(default=None, description="Public or private Provider.")
    ]
    connection_url: Annotated[
        str | None, Field(default=None, description="Provider connection URL.")
    ]
