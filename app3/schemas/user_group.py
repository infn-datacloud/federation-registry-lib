from pydantic import BaseModel


class UserGroupBase(BaseModel):
    """UserGroup Base class.

    Class without id (which is populated by the database).

    Attributes:
        name (str): UserGroup name.
        description (str): Brief description.
    """

    name: str
    description: str = ""

    class Config:
        validate_assignment = True


class UserGroupCreate(UserGroupBase):
    """UserGroup Create class.

    Class without id (which is populated by the database).
    expected as input when performing a REST request.

    Attributes:
        name (str): UserGroup name.
        description (str): Brief description.
    """

    pass


class UserGroup(UserGroupBase):
    """UserGroup class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): UserGroup unique ID.
        name (str): UserGroup name.
        description (str): Brief description.
    """

    uid: str

    class Config:
        orm_mode = True
