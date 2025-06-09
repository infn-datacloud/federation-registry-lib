"""Pydantic models of the Provider - Identity Provider relationship."""

from pydantic import BaseModel, Field

from fedreg.auth_method.constants import DOC_AUD, DOC_IDP_NAME, DOC_PROTOCOL
from fedreg.core import BaseNodeCreate


class AuthMethodOsCreate(BaseNodeCreate, BaseModel):
    """Model with the basic attributes used by the AuthMethod relationship.

    Attributes:
    ----------
        idp_name (str): Identity Provider name saved in the Resource Provider.
        protocol (str): Protocol to use when authenticating on this identity
            provider.
    """

    idp_name: str = Field(description=DOC_IDP_NAME)
    protocol: str = Field(description=DOC_PROTOCOL)


class AuthMethodK8sCreate(BaseNodeCreate, BaseModel):
    """Model to create an AuthMethod instance.

    Class expected as input when performing a POST request.

    Attributes:
    ----------
        audience (str): Audience to use when authenticating on this identity
            provider.
    """

    audience: str = Field(description=DOC_AUD)


class AuthMethodRead(BaseModel):
    """Model to read AuthMethod relationship data retrieved from the DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request.

    Attributes:
    ----------
        idp_name (str | None): Identity Provider name saved in the Resource Provider.
        protocol (str | None): Protocol to use when authenticating on this identity
            provider.
        audience (str | None): Audience to use when authenticating on this identity
            provider.
    """

    idp_name: str | None = Field(default=None, description=DOC_IDP_NAME)
    protocol: str | None = Field(default=None, description=DOC_PROTOCOL)
    audience: str | None = Field(default=None, description=DOC_AUD)

    class Config:
        """Sub class to validate assignments and enable orm mode.

        Use ORM mode to read data from DB models.
        """

        validate_assignment = True
        orm_mode = True
