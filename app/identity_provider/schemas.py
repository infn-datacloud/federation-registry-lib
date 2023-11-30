"""Identity Provider pydantic models."""
from typing import Optional

from pydantic import AnyHttpUrl, Field

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class IdentityProviderBase(BaseNode):
    """Model with Identity Provider basic attributes.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): value of the key from which retrieve
            the user group name from an authentication token.
    """

    endpoint: AnyHttpUrl = Field(description="URL of the identity provider")
    group_claim: str = Field(
        description="Name to use to retrieve the user's group attribute"
    )


class IdentityProviderCreate(BaseNodeCreate, IdentityProviderBase):
    """Model to create an Identity Provider.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): value of the key from which retrieve
            the user group name from an authentication token.
    """


class IdentityProviderUpdate(BaseNodeCreate, IdentityProviderBase):
    """Model to update an Identity Provider.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        endpoint (str | None): URL of the Identity Provider.
        group_claim (str | None): value of the key from which retrieve
            the user group name from an authentication token.
    """

    endpoint: Optional[AnyHttpUrl] = Field(
        default=None, description="URL of the identity provider"
    )
    group_claim: Optional[str] = Field(
        default=None,
        description="Name to use to retrieve the user's group attribute",
    )


class IdentityProviderRead(BaseNodeRead, IdentityProviderBase):
    """Model to read Identity Provider data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): value of the key from which retrieve
            the user group name from an authentication token.
    """


class IdentityProviderReadPublic(BaseNodeRead, IdentityProviderBase):
    pass


class IdentityProviderReadShort(BaseNodeRead, IdentityProviderBase):
    pass


IdentityProviderQuery = create_query_model(
    "IdentityProviderQuery", IdentityProviderBase
)
