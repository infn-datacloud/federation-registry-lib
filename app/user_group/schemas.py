from pydantic import BaseModel

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class UserGroupBase(BaseModel):
    name: str


class UserGroupCreate(BaseNodeCreate, UserGroupBase):
    """UserGroup Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        name (str): UserGroup name.
    """


class UserGroupUpdate(UserGroupCreate):
    """UserGroup Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

    Attributes:
        description (str): Brief description.
        name (str | None): UserGroup name.
    """


class UserGroupRead(BaseNodeRead, UserGroupBase):
    """UserGroup class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        name (str): UserGroup name.
    """


UserGroupQuery = create_query_model("UserGroupQuery", UserGroupBase)
