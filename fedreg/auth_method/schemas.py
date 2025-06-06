"""Pydantic models of the Provider - Identity Provider relationship."""

from typing import Annotated

from pydantic import BaseModel, Field

from fedreg.core import BaseNodeRead
from fedreg.identity_provider.schemas import IdentityProviderBase


class AuthMethodBase(BaseModel):
    """Model with the basic attributes used by the AuthMethod relationship.

    Attributes:
    ----------
        idp_name (str): Identity Provider name saved in the Resource Provider.
        protocol (str): Protocol to use when authenticating on this identity provider
        audience (str): Audience to use when authenticating on this identity provider.
    """

    idp_name: Annotated[
        str | None,
        Field(
            default=None,
            description="Identity Provider name saved in the Resource Provider.",
        ),
    ]
    protocol: Annotated[
        str | None,
        Field(
            default=None,
            description="Protocol to use when authenticating on target IdP.",
        ),
    ]
    audience: Annotated[
        str | None,
        Field(
            default=None,
            description="Audience to use when authenticating on target IdP.",
        ),
    ]


class AuthMethodCreate(AuthMethodBase):
    """Schema for creating a new authentication method.

    Inherits from:
        AuthMethodBase: Base schema with common authentication method fields.

    Attributes:
        Inherits all fields from AuthMethodBase.
    """


class AuthMethodRead(BaseNodeRead, IdentityProviderBase):
    """Represents a read-only schema for authentication methods

    Combines base node read attributes and identity provider base information.

    Inherits from:
        BaseNodeRead: Provides base attributes for node reading operations.
        IdentityProviderBase: Supplies identity provider-specific fields.

    Attributes:
        Inherits all attributes from BaseNodeRead and IdentityProviderBase.
    """
