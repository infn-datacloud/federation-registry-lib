from pydantic import AnyHttpUrl
from typing import Optional

from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class IdentityProviderQuery(BaseNodeQuery):
    """IdentityProvider Query Model class.

    Attributes:
        description (str | None): Brief description.
        endpoint (str | None): URL of the IdentityProvider.
    """

    endpoint: Optional[AnyHttpUrl] = None
    group_claim: Optional[str] = None


class IdentityProviderCreate(BaseNodeCreate):
    """IdentityProvider Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    endpoint: AnyHttpUrl
    group_claim: str


class IdentityProviderUpdate(IdentityProviderCreate):
    """IdentityProvider Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        endpoint (str | None): URL of the IdentityProvider.
    """


class IdentityProvider(BaseNodeRead, IdentityProviderCreate):
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
