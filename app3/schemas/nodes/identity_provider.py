from pydantic import AnyUrl
from typing import Optional

from ..utils.base_model import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class IdentityProviderQuery(BaseNodeQuery):
    """IdentityProvider Query Model class.

    Attributes:
        description (str | None): Brief description.
        endpoint (str | None): URL of the IdentityProvider.
    """

    endpoint: Optional[AnyUrl] = None


class IdentityProviderPatch(BaseNodeCreate):
    """IdentityProvider Patch Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        endpoint (str | None): URL of the IdentityProvider.
    """

    endpoint: Optional[AnyUrl] = None


class IdentityProviderCreate(IdentityProviderPatch):
    """IdentityProvider Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    endpoint: AnyUrl


class IdentityProvider(IdentityProviderCreate, BaseNodeRead):
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
