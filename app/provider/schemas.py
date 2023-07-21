from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class ProviderBase(BaseModel):
    name: str
    is_public: bool = False
    support_emails: List[EmailStr] = Field(default_factory=list)


class ProviderCreate(BaseNodeCreate, ProviderBase):
    """Provider Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        name (str): Provider name (type).
        is_public (bool): Public or private provider.
        support_emails (list of str): List of maintainers emails.
    """


class ProviderUpdate(ProviderCreate):
    """Provider Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

    Attributes:
        description (str | None): Brief description.
        name (str | None): Provider name (type).
        is_public (bool | None): Public or private provider.
        support_email (list of str | None): List of maintainers emails.
        location (LocationCreate | None): provider physical location
        clusters TODO
        flavors TODO
        identity_providers TODO
        images TODO
        projects TODO
        services TODO
    """


class ProviderRead(BaseNodeRead, ProviderBase):
    """Provider class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        name (str): Provider name (type).
        is_public (bool): Public or private provider.
        support_emails (list of str): List of maintainers emails.
    """


ProviderQuery = create_query_model("ProviderQuery", ProviderBase)
