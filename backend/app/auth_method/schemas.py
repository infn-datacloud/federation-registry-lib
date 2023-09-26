from pydantic import BaseModel, Field


class AuthMethodBase(BaseModel):
    """Model with a Provider Authentication Method basic attributes.

    Always validate assignments.
    """

    idp_name: str = Field(
        description="Identity Provider name used by the provider \
            to authenticate."
    )
    protocol: str = Field(
        description="Communication protocol used by the provider \
            to authenticate."
    )

    class Config:
        validate_assignment = True


class AuthMethodCreate(AuthMethodBase):
    """Model to create a Provider Authentication Method.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class AuthMethodRead(AuthMethodBase):
    """Model to read Provider Authentication Method data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Use ORM mode to read data from DB models. Always validate
    assignments.
    """

    class Config:
        validate_assignment = True
        orm_mode = True
