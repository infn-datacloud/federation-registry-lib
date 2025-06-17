"""Pydantic extended models of the Identity Provider."""

from pydantic import Field

from fedreg.v1.auth_method.schemas import AuthMethodRead
from fedreg.v1.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.v1.identity_provider.constants import DOC_EXT_GROUP, DOC_EXT_PROV
from fedreg.v1.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fedreg.v1.provider.constants import DOC_EXT_AUTH_METH
from fedreg.v1.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.v1.user_group.schemas import UserGroupRead, UserGroupReadPublic


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
        support_email (list of str): list of maintainers emails.
        relationship (AuthMethodRead): Authentication method used to connect to the
            target identity provider.
    """

    relationship: AuthMethodRead = Field(description=DOC_EXT_AUTH_METH)


class ProviderReadExtendedPublic(ProviderReadPublic):
    """Model to extend the Identity Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        relationship (AuthMethodRead): Authentication method used to connect to the
            target identity provider.
    """

    relationship: AuthMethodRead = Field(description=DOC_EXT_AUTH_METH)


class IdentityProviderReadExtended(BaseReadPrivateExtended, IdentityProviderRead):
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

    providers: list[ProviderReadExtended] = Field(
        default_factory=list, description=DOC_EXT_PROV
    )
    user_groups: list[UserGroupRead] = Field(
        default_factory=list, description=DOC_EXT_GROUP
    )


class IdentityProviderReadExtendedPublic(
    BaseReadPublicExtended, IdentityProviderReadPublic
):
    """Model to extend the Identity Provider public data read from the DB.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        providers (list of ProviderReadExtendedPublic): Supported providers.
        user_groups (list of UserGroupReadPublic): Owned user groups.
    """

    providers: list[ProviderReadExtendedPublic] = Field(
        default_factory=list, description=DOC_EXT_PROV
    )
    user_groups: list[UserGroupReadPublic] = Field(
        default_factory=list, description=DOC_EXT_GROUP
    )
