from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class LocationBase(BaseModel):
    """Location Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): Location unique name.
        description (str): Brief description.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        validate_assignment = True


class LocationUpdate(LocationBase):
    """Location Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        name (str): Location unique name.
        description (str): Brief description.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    description: str = ""


class LocationCreate(LocationUpdate):
    """Location Create class.

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        name (str): Location unique name.
        description (str): Brief description.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    name: str
    country: str
    country_code: str


class Location(LocationCreate):
    """Location class

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Location unique ID.
        name (str): Location unique name.
        description (str): Brief description.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    uid: UUID

    class Config:
        orm_mode = True
