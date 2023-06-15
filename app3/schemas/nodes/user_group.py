from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class UserGroupBase(BaseModel):
    """UserGroup Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): UserGroup name.
        description (str): Brief description.
    """

    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        validate_assignment = True


class UserGroupUpdate(UserGroupBase):
    """UserGroup Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): UserGroup name.
        description (str): Brief description.
    """

    description: str = ""


class UserGroupCreate(UserGroupUpdate):
    """UserGroup Create class.

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        name (str): UserGroup name.
        description (str): Brief description.
    """

    name: str


class UserGroup(UserGroupCreate):
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

    uid: UUID

    class Config:
        orm_mode = True
