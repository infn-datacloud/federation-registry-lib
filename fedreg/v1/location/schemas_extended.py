"""Pydantic extended models of the site geographical Location."""

from pydantic import Field

from fedreg.v1.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.v1.location.constants import DOC_EXT_REG
from fedreg.v1.location.schemas import (
    LocationRead,
    LocationReadPublic,
)
from fedreg.v1.region.schemas import RegionRead, RegionReadPublic


class LocationReadExtended(BaseReadPrivateExtended, LocationRead):
    """Model to extend the Location data read from the DB.

    Attributes:
    ----------
        uid (int): Location unique ID.
        description (str): Brief description.
        site (str): Location unique name.
        country (str): Country name.
        country_code (str): Country code with 3 chars.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
        regions (list of RegionRead): Hosted regions.
    """

    regions: list[RegionRead] = Field(default_factory=list, description=DOC_EXT_REG)


class LocationReadExtendedPublic(BaseReadPublicExtended, LocationReadPublic):
    """Model to extend the Location public data read from the DB.

    Attributes:
    ----------
        uid (int): Location unique ID.
        description (str): Brief description.
        site (str): Location unique name.
        regions (list of RegionReadPublic): Hosted regions.
    """

    regions: list[RegionReadPublic] = Field(
        default_factory=list, description=DOC_EXT_REG
    )
