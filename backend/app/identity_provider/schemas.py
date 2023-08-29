from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import AnyHttpUrl, BaseModel, Field


class IdentityProviderBase(BaseModel):
    """Model with Identity Provider basic attributes."""

    endpoint: AnyHttpUrl = Field(description="URL of the identity provider")
    group_claim: str = Field(
        description="Name to use to retrieve the user's group attribute"
    )


class IdentityProviderCreate(BaseNodeCreate, IdentityProviderBase):
    """Model to create an Identity Provider.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.
    """


class IdentityProviderUpdate(IdentityProviderCreate):
    """Model to update a Identity Provider.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

    Default to None mandatory attributes.
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

    Class to read data retrieved from the database.
    Expected as output when performing a generic REST request.
    It contains all the non-sensible data written in the database.

    Add the *uid* attribute, which is the item unique
    identifier in the database.
    """


IdentityProviderQuery = create_query_model(
    "IdentityProviderQuery", IdentityProviderBase
)
