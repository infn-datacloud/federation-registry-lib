from pydantic import BaseModel


class LocationBase(BaseModel):
    """Location Base class.

    Class without id (which is populated by the database).

    Attributes:
        name (str): Location unique name.
        description (str): Brief description.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    name: str
    description: str = ""
    country: str
    country_code: str
    latitude: float
    longitude: float

    class Config:
        validate_assignment = True


class LocationCreate(LocationBase):
    """Location Create class.

    Class without id (which is populated by the database).
    expected as input when performing a REST request.

    Attributes:
        name (str): Location unique name.
        description (str): Brief description.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    pass


class Location(LocationBase):
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

    uid: str

    class Config:
        orm_mode = True
