"""Pydantic models of the site geographical Location."""
from typing import Any, Dict, Optional

from pycountry import countries
from pydantic import Field, root_validator, validator

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class LocationBase(BaseNode):
    """Model with Location basic attributes.

    Attributes:
    ----------
        description (str): Brief description.
        site (str): Location unique name.
        country (str): Country name.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
    """

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
        """Validate country."""
        assert v in [i.name for i in countries]
        return v


class LocationCreate(BaseNodeCreate, LocationBase):
    """Model to create a Location.

    Class without id (which is populated by the database). Expected as input when
    performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        site (str): Location unique name.
        country (str): Country name.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
    """


class LocationUpdate(BaseNodeCreate, LocationBase):
    """Model to update a Location.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        site (str | None): Location unique name.
        country (str | None): Country name.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
    """

    site: Optional[str] = Field(
        default=None, description="Name of the Location hosting a provider."
    )
    country: Optional[str] = Field(default=None, description="Location's country name.")


class LocationRead(BaseNodeRead, LocationBase):
    """Model to read Location data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database. Add
    the *country_code* attribute.

    Attributes:
    ----------
        uid (int): Location unique ID.
        description (str): Brief description.
        site (str): Location unique name.
        country (str): Country name.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
    """

    country_code: Optional[str] = Field(
        default=None, description="Country code with 3 char"
    )

    @root_validator(pre=True)
    def get_country_code(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """From country retrieve country code."""
        matches = countries.search_fuzzy(values["country"])
        if len(matches) > 0:
            values["country_code"] = matches[0].alpha_3
        return values


class LocationReadPublic(BaseNodeRead, LocationBase):
    pass


class LocationReadShort(BaseNodeRead, LocationBase):
    pass


LocationQuery = create_query_model("LocationQuery", LocationBase)
