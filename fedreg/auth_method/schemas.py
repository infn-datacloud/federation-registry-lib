"""Pydantic models of the Provider - Identity Provider relationship."""

from pydantic import BaseModel, Field

from fedreg.auth_method.constants import DOC_AUD, DOC_IDP_NAME, DOC_PROTOCOL
from fedreg.core import BaseNodeCreate


class AuthMethodBase(BaseModel):
    """Model with the basic attributes used by the AuthMethod relationship.

    Attributes:
    ----------
        idp_name (str | None): Identity Provider name saved in the Resource Provider.
        protocol (str | None): Protocol to use when authenticating on this identity
            provider.
        aud (str | None): Audience to use when authenticating on this identity provider.
    """

    idp_name: str | None = Field(default=None, description=DOC_IDP_NAME)
    protocol: str | None = Field(default=None, description=DOC_PROTOCOL)
    aud: str | None = Field(default=None, description=DOC_AUD)


class AuthMethodCreate(BaseNodeCreate, AuthMethodBase):
    """Model to create an AuthMethod instance.

    Class expected as input when performing a POST request.

    Attributes:
    ----------
        idp_name (str | None): Identity Provider name saved in the Resource Provider.
        protocol (str | None): Protocol to use when authenticating on this identity
            provider.
        aud (str | None): Audience to use when authenticating on this identity provider.
    """


class AuthMethodRead(AuthMethodBase):
    """Model to read AuthMethod relationship data retrieved from the DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request.

    Attributes:
    ----------
        idp_name (str | None): Identity Provider name saved in the Resource Provider.
        protocol (str | None): Protocol to use when authenticating on this identity
            provider.
        aud (str | None): Audience to use when authenticating on this identity provider.
    """

    class Config:
        """Sub class to validate assignments and enable orm mode.

        Use ORM mode to read data from DB models.
        """

        validate_assignment = True
        orm_mode = True
