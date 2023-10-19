from typing import Dict, Optional

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pycountry import countries
from pydantic import Field, root_validator, validator


class LocationBase(BaseNode):
    """Model with Location basic attributes."""

    site: str = Field(description="Name of the Location hosting a provider.")
    country: str = Field(description="Location's country name.")
    latitude: Optional[float] = Field(
        default=None, ge=-180, le=180, description="Latitude coordinate."
    )
    longitude: Optional[float] = Field(
        default=None, ge=-90, le=90, description="Longitude coordinate."
    )

    @validator("country")
    def is_known_country(cls, v) -> str:
        assert v in [i.name for i in countries]
        return v


class LocationCreate(BaseNodeCreate, LocationBase):
    """Model to create a Location.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class LocationUpdate(BaseNodeCreate, LocationBase):
    """Model to update a Location.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    site: Optional[str] = Field(
        default=None, description="Name of the Location hosting a provider."
    )
    country: Optional[str] = Field(default=None, description="Location's country name.")


class LocationRead(BaseNodeRead, LocationBase):
    """Model to read Location data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database. Add the *country_code* attribute.
    """

    country_code: Optional[str] = Field(
        default=None, description="Country code with 3 char"
    )

    @root_validator(pre=True)
    def get_country_code(cls, values: Dict) -> Dict:
        matches = countries.search_fuzzy(values["country"])
        if len(matches) > 0:
            values["country_code"] = matches[0].alpha_3
        return values


class LocationReadPublic(BaseNodeRead, LocationBase):
    pass


class LocationReadShort(BaseNodeRead, LocationBase):
    pass


LocationQuery = create_query_model("LocationQuery", LocationBase)
