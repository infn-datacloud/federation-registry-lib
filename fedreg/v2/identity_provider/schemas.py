"""Pydantic models of the Identity Provider."""

from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, Field

from fedreg.v2.core import BaseNode, BaseNodeRead, PaginationQuery


class IdentityProviderBase(BaseNode):
    """Base schema for an Identity Provider node.

    Attributes:
        endpoint (AnyHttpUrl): Issuer URL as defined in the introspection endpoint.
        group_claim (str): Value of the key from which to retrieve the user group name
            from an authentication token.
    """

    endpoint: Annotated[
        AnyHttpUrl,
        Field(description="Issuer URL as defined in the introspection endpoint."),
    ]
    group_claim: Annotated[
        str,
        Field(
            description="Value of the key from which retrieve the user group name from "
            "an authentication token."
        ),
    ]


class IdentityProviderCreate(IdentityProviderBase):
    """Schema for creating a new Identity Provider.

    Inherits from:
        IdentityProviderBase: Base schema with common fields for Identity Providers.

    Use this schema to validate and serialize data when creating a new Identity Provider
    instance.
    """


class IdentityProviderLinks(BaseModel):
    """
    Schema representing the links related to an Identity Provider.

    Attributes:
        user_groups (AnyHttpUrl): Link to the Identity Provider's user groups endpoint.
    """

    user_groups: Annotated[
        AnyHttpUrl,
        Field(description="Link to the Identity Provider's user groups endpoint."),
    ]


class IdentityProviderRead(BaseNodeRead, IdentityProviderBase):
    """Represents a read-only view of an Identity Provider

    Includes its associated user groups and relevant links.

    Inherits from:
        BaseNodeRead: Base class for node read operations.
        IdentityProviderBase: Base schema for Identity Provider attributes.

    Attributes:
        user_groups (list[str]): List of user group IDs belonging to the Identity
            Provider.
        links (IdentityProviderLinks): Dictionary with links to the IdP's user groups
            endpoint.
    """

    user_groups: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of user group IDs belonging to the Identity Provider.",
        ),
    ]
    links: Annotated[
        IdentityProviderLinks,
        Field(description="Dictionary with links to the IdP's user groups endpoint."),
    ]


class IdentityProviderQuery(PaginationQuery):
    """Schema for querying identity providers.

    Overrides the endpoint field to be a simple string.

    Inherits from:
        IdentityProviderBase: Provides common fields for Identity Providers.

    Attributes:
        endpoint (str): Issuer URL as defined in the introspection endpoint.
    """

    endpoint: Annotated[
        str | None,
        Field(
            default=None,
            description="Issuer URL as defined in the introspection endpoint.",
        ),
    ]
    group_claim: Annotated[
        str | None,
        Field(
            default=None,
            description="Value of the key from which retrieve the user group name from "
            "an authentication token.",
        ),
    ]
