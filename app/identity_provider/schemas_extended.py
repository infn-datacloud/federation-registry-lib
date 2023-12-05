"""Pydantic extended models of the Identity Provider."""
from typing import List

from pydantic import Field

from app.auth_method.schemas import AuthMethodRead
from app.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from app.provider.schemas import ProviderRead, ProviderReadPublic
from app.user_group.schemas import UserGroupRead, UserGroupReadPublic


class ProviderReadExtended(ProviderRead):
    """Model to extend the Provider data read from the DB.

    Add the authentication method data used by this provider to connect to the target
    identity provider.
    """

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Identity Provider public data read from the DB.

    Add the authentication method data used by this provider to connect to the target
    identity provider.
    """

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB.

    Add the lists of providers and user groups.
    """

    providers: List[ProviderReadExtended] = Field(
        description="List of supported providers."
    )
    user_groups: List[UserGroupRead] = Field(description="List of owned user groups.")


class IdentityProviderReadExtendedPublic(IdentityProviderReadPublic):
    """Model to extend the Identity Provider public data read from the DB.

    Add the lists of providers and user groups.
    """

    providers: List[ProviderReadExtendedPublic] = Field(
        description="List of supported providers."
    )
    user_groups: List[UserGroupReadPublic] = Field(
        description="List of owned user groups."
    )
