from pydantic import BaseModel, Extra


class AuthMethodBase(BaseModel):
    idp_name: str
    protocol: str

    class Config:
        validate_assignment = True
        extra = Extra.ignore


class AuthMethodCreate(AuthMethodBase):
    """AuthMethod Create class

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.


    Attributes:
        idp_name (str): Identity Provider name saved in the Provider.
        protocol (str): Protocol to use when authenticating on this
            identity provider.
    """


class AuthMethodUpdate(AuthMethodCreate):
    """AuthMethod Base class

    Class without id (which is populated by the database).
    Expected as input when performing a PUT REST request.

    Attributes:
        idp_name (str): Identity Provider name saved in the Provider.
        protocol (str): Protocol to use when authenticating on this
            identity provider.
    """


class AuthMethodRead(AuthMethodBase):
    """AuthMethod class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        idp_name (str): Identity Provider name saved in the Provider.
        protocol (str): Protocol to use when authenticating on this
            identity provider.
    """

    class Config:
        orm_mode = True
