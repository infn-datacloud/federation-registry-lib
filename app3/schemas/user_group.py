from pydantic import BaseModel, Field
from typing import List

# from .project import Project


class UserGroupBase(BaseModel):
    """UserGroup Base class.

    Class without id which is populated by the database.

    Attributes:
        name (str): UserGroup name.
        projects (list of Projects): Lists of projects owned by a UserGroup.
    """

    name: str
    description: str = ""
    # projects: List[Project] = Field(default_factory=list)

    class Config:
        validate_assignment = True


class UserGroupCreate(UserGroupBase):
    """UserGroup Create class.

    Class expected as input when performing a REST request.

    Attributes:
        name (str): UserGroup name.
        projects (list of Projects): Lists of projects owned by a UserGroup.
    """

    pass


class UserGroup(UserGroupBase):
    """UserGroup class

    Class expected as output when performing a REST request.
    It contains all the non-sensible data written in the database.

    Attributes:
        uid (str): UserGroup unique ID.
        name (str): UserGroup name.
        projects (list of Projects): Lists of projects owned by a UserGroup.
    """

    uid: str

    class Config:
        orm_mode = True
