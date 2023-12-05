"""Region owned by a Provider pydantic models."""
from typing import Optional

from pydantic import Field

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class RegionBase(BaseNode):
    """Model with Region basic attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
    """

    name: str = Field(description="Region name in the provider.")


class RegionCreate(BaseNodeCreate, RegionBase):
    """Model to create a Region.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
    """


class RegionUpdate(BaseNodeCreate, RegionBase):
    """Model to update a Region.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): Name of the Region in the Provider.
    """

    name: Optional[str] = Field(
        default=None, description="Region name in the provider."
    )


class RegionRead(BaseNodeRead, RegionBase):
    """Model to read Region data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
    """


class RegionReadPublic(BaseNodeRead, RegionBase):
    pass


class RegionReadShort(BaseNodeRead, RegionBase):
    pass


RegionQuery = create_query_model("RegionQuery", RegionBase)
