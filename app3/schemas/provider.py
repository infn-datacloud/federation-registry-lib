from pydantic import BaseModel, Field
from typing import List, Optional


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
    description: str = ""
    is_public: bool = False
    support_email: List[str] = Field(default_factory=list)

    class Config:
        validate_assignment = True


class ProviderCreate(ProviderBase):
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


class Provider(ProviderBase):
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

    uid: str

    class Config:
        orm_mode = True
