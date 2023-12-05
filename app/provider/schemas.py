"""Pydantic models of the Resource Provider (openstack, kubernetes...)."""
from typing import List, Optional

from pydantic import EmailStr, Field

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.provider.enum import ProviderStatus, ProviderType
from app.query import create_query_model


class ProviderBase(BaseNode):
    """Model with Provider basic attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): List of maintainers emails.
    """

    name: str = Field(description="Provider name.")
    type: ProviderType = Field(description="Provider type.")
    status: ProviderStatus = Field(
        default=ProviderStatus.ACTIVE, description="Provider status"
    )
    is_public: bool = Field(default=False, description="It is a public provider.")
    support_emails: List[EmailStr] = Field(
        default_factory=list, description="Contact emails."
    )


class ProviderCreate(BaseNodeCreate, ProviderBase):
    """Model to create a Provider.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): List of maintainers emails.
    """


class ProviderUpdate(BaseNodeCreate, ProviderBase):
    """Model to update a Provider.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): Provider name.
        type (str | None): Provider type.
        status (str | None): Provider status.
        is_public (bool | None): Public or private Provider.
        support_email (list of str | None): List of maintainers emails.
    """

    name: Optional[str] = Field(default=None, description="Provider name.")
    type: Optional[ProviderType] = Field(default=None, description="Provider type.")


class ProviderRead(BaseNodeRead, ProviderBase):
    """Model to read Provider data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): List of maintainers emails.
    """


class ProviderReadPublic(BaseNodeRead, ProviderBase):
    pass


class ProviderReadShort(BaseNodeRead, ProviderBase):
    pass


ProviderQuery = create_query_model("ProviderQuery", ProviderBase)
