from uuid import UUID
from pydantic import BaseModel


class IdentityProviderBase(BaseModel):
    """IdentityProvider Base class.

    Class without id which is populated by the database.

    Attributes:
        name (str): Identity provider name.
        url (str): Identity provider url.
        protocol (str): Identity provider protocol.
    """

    name: str
    url: str
    protocol: str

    class Config:
        validate_assignment = True


class IdentityProviderCreate(IdentityProviderBase):
    """IdentityProvider Create class.

    Class expected as input when performing a REST request.

    Attributes:
        name (str): Identity provider name.
        url (str): Identity provider url.
        protocol (str): Identity provider protocol.
    """

    pass


class IdentityProvider(IdentityProviderBase):
    """IdentityProvider class

    Class expected as output when performing a REST request.
    It contains all the non-sensible data written in the database.

    Attributes:
        id (str): Identity provider unique ID.
        name (str): Identity provider name.
        url (str): Identity provider url.
        protocol (str): Identity provider protocol.
    """

    id: UUID

    class Config:
        orm_mode = True
