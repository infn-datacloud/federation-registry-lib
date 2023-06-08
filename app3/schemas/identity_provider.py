from pydantic import BaseModel
from typing import Optional


class IdentityProviderBase(BaseModel):
    """IdentityProvider Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    description: str = ""
    endpoint: Optional[str] = None

    class Config:
        validate_assignment = True


class IdentityProviderCreate(IdentityProviderBase):
    """IdentityProvider Create class.

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    endpoint: str


class IdentityProvider(IdentityProviderBase):
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

    uid: str

    class Config:
        orm_mode = True
