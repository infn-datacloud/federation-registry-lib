from typing import List

from app.location.schemas import LocationRead
from app.provider.schemas import ProviderRead
from pydantic import Field


class LocationReadExtended(LocationRead):
    """Model to extend the Location data read from the
    DB with the lists of related items.
    """

    providers: List[ProviderRead] = Field(
        default_factory=list, description="List of hosted providers."
    )
