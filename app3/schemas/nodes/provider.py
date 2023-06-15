from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class ProviderBase(BaseModel):
    """Provider Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    support_email: Optional[List[str]] = None

    class Config:
        validate_assignment = True


class ProviderUpdate(ProviderBase):
    """Provider Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    description: str = ""
    is_public: bool = False
    support_email: List[str] = Field(default_factory=list)


class ProviderCreate(ProviderUpdate):
    """Provider Create class

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    name: str


class Provider(ProviderCreate):
    """Provider class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Provider unique ID.
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    uid: UUID

    class Config:
        orm_mode = True
