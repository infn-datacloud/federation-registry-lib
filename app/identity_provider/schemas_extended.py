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

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): List of maintainers emails.
        relationship (AuthMethodRead): Authentication method used to connect to the
            target identity provider.
    """

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Identity Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): List of maintainers emails.
        relationship (AuthMethodRead): Authentication method used to connect to the
            target identity provider.
    """

    relationship: AuthMethodRead = Field(
        description="Authentication method used by the Provider"
    )


class IdentityProviderReadExtended(IdentityProviderRead):
    """Model to extend the Identity Provider data read from the DB.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): value of the key from which retrieve
            the user group name from an authentication token.
        providers (list of ProviderReadExtended): Supported providers.
        user_groups (list of UserGroupRead): Owned user groups.
    """

    providers: List[ProviderReadExtended] = Field(
        description="List of supported providers."
    )
    user_groups: List[UserGroupRead] = Field(description="List of owned user groups.")


class IdentityProviderReadExtendedPublic(IdentityProviderReadPublic):
    """Model to extend the Identity Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): value of the key from which retrieve
            the user group name from an authentication token.
        providers (list of ProviderReadExtendedPublic): Supported providers.
        user_groups (list of UserGroupReadPublic): Owned user groups.
    """

    providers: List[ProviderReadExtendedPublic] = Field(
        description="List of supported providers."
    )
    user_groups: List[UserGroupReadPublic] = Field(
        description="List of owned user groups."
    )
