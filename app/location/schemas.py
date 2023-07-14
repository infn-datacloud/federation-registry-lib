from pycountry import countries
from pydantic import BaseModel, Field, root_validator
from typing import Dict, Optional

from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class LocationBase(BaseModel):
    name: str
    country: str
    latitude: Optional[float] = Field(ge=-180, le=180, default=None)
    longitude: Optional[float] = Field(ge=-90, le=90, default=None)


class LocationQuery(BaseNodeQuery):
    """Location BQuery Model class.

    Attributes:
        description (str | None): Brief description.
        name (str | None): Location unique name.
        country (str | None): Country name.
        country_code (str | None): Country code.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
    """

    name: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    latitude: Optional[float] = Field(ge=-180, le=180, default=None)
    longitude: Optional[float] = Field(ge=-90, le=90, default=None)


class LocationCreate(BaseNodeCreate, LocationBase):
    """Location Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        name (str): Location unique name.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
    """


class LocationUpdate(LocationCreate):
    """Location Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        name (str | None): Location unique name.
        country (str | None): Country name.
        country_code (str | None): Country code.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
    """


class LocationRead(BaseNodeRead, LocationBase):
    """Location class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        description (str): Brief description.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    country_code: str

    @root_validator(pre=True)
    def get_country_code(cls, values: Dict) -> Dict:
        matches = countries.search_fuzzy(values["country"])
        values["country_code"] = matches[0].alpha_3
        return values
