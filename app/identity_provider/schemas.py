from pydantic import AnyHttpUrl, BaseModel
from typing import Optional

from app.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class IdentityProviderBase(BaseModel):
    endpoint: AnyHttpUrl
    group_claim: str


class IdentityProviderQuery(BaseNodeQuery):
    """IdentityProvider Query Model class.

    Attributes:
        description (str | None): Brief description.
        endpoint (str | None): URL of the IdentityProvider.
    """

    endpoint: Optional[AnyHttpUrl] = None
    group_claim: Optional[str] = None


class IdentityProviderCreate(BaseNodeCreate, IdentityProviderBase):
    """IdentityProvider Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """


class IdentityProviderUpdate(IdentityProviderCreate):
    """IdentityProvider Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        endpoint (str | None): URL of the IdentityProvider.
    """


class IdentityProviderRead(BaseNodeRead, IdentityProviderBase):
    """IdentityProvider class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """
