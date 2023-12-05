"""Pydantic extended models of the site geographical Location."""
from typing import List

from pydantic import Field

from app.location.schemas import LocationRead, LocationReadPublic
from app.region.schemas import RegionRead, RegionReadPublic


class LocationReadExtended(LocationRead):
    """Model to extend the Location data read from the DB.

    Add the list of regions.
    """

    regions: List[RegionRead] = Field(description="List of hosted regions.")


class LocationReadExtendedPublic(LocationReadPublic):
    """Model to extend the Location public data read from the DB.

    Add the list of regions.
    """

    regions: List[RegionReadPublic] = Field(description="List of hosted regions.")
