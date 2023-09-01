from typing import List

from app.location.schemas import LocationRead, LocationReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from pydantic import Field


class LocationReadExtended(LocationRead):
    """Model to extend the Location data read from the DB with the lists of
    related items for authenticated users."""

    providers: List[ProviderRead] = Field(
        default_factory=list, description="List of hosted providers."
    )


class LocationReadExtendedPublic(LocationReadPublic):
    """Model to extend the Location data read from the DB with the lists of
    related items for non-authenticated users."""

    providers: List[ProviderReadPublic] = Field(
        default_factory=list, description="List of hosted providers."
    )
