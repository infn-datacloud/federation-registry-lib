from typing import List

from app.auth_method.schemas import AuthMethodRead
from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic
from pydantic import Field


class ProviderReadExtended(ProviderRead):
    """Model to extend the Provider data read from the DB with the authentication method
    details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Provider data read from the DB with the authentication method
    details."""

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB with the lists of
    related items for authenticated users."""

    providers: List[ProviderReadExtended] = Field(
        default_factory=list, description="List of supported providers."
    )
    user_groups: List[UserGroupRead] = Field(
        default_factory=list, description="List of owned user groups."
    )


class IdentityProviderReadExtendedPublic(IdentityProviderReadPublic):
    """Model to extend the Identity Provider data read from the DB with the lists of
    related items for non-authenticated users."""

    providers: List[ProviderReadExtendedPublic] = Field(
        default_factory=list, description="List of supported providers."
    )
    user_groups: List[UserGroupReadPublic] = Field(
        default_factory=list, description="List of owned user groups."
    )
