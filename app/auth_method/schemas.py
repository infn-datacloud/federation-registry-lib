"""Pydantic models of the Provider - Identity Provider relationship."""
from pydantic import BaseModel, Field


class AuthMethodBase(BaseModel):
    """Model with a Provider Authentication Method basic attributes.

    Attributes:
    ----------
        idp_name (str): Identity Provider name used by the provider to authenticate.
        protocol (str): Communication protocol used by the provider to authenticate.
    """

    idp_name: str = Field(
        description="Identity Provider name used by the provider to authenticate."
    )
    protocol: str = Field(
        description="Communication protocol used by the provider to authenticate."
    )

    class Config:
        """Sub class to validate assignments."""

        validate_assignment = True


class AuthMethodCreate(AuthMethodBase):
    """Model to create a Provider Authentication Method.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        idp_name (str): Identity Provider name used by the provider to authenticate.
        protocol (str): Communication protocol used by the provider to authenticate.
    """


class AuthMethodRead(AuthMethodBase):
    """Model to read Provider Authentication Method data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non-sensible data written in the
    database.

    Use ORM mode to read data from DB models. Always validate assignments.

    Attributes:
    ----------
        idp_name (str): Identity Provider name used by the provider to authenticate.
        protocol (str): Communication protocol used by the provider to authenticate.
    """

    class Config:
        """Sub class to validate assignments and enable orm mode."""

        validate_assignment = True
        orm_mode = True
