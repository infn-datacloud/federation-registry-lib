from pydantic import AnyUrl, BaseModel
from typing import Optional
from uuid import UUID


class IdentityProviderBase(BaseModel):
    """IdentityProvider Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    description: Optional[str] = None
    endpoint: Optional[AnyUrl] = None

    class Config:
        validate_assignment = True


class IdentityProviderUpdate(IdentityProviderBase):
    """IdentityProvider Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    description: str = ""


class IdentityProviderCreate(IdentityProviderUpdate):
    """IdentityProvider Create class.

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    endpoint: AnyUrl


class IdentityProvider(IdentityProviderCreate):
    """IdentityProvider class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Identity provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    uid: UUID

    class Config:
        orm_mode = True
