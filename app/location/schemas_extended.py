from pydantic import Field
from typing import List

from app.location.schemas import LocationRead
from app.provider.schemas import ProviderRead


class LocationReadExtended(LocationRead):
    providers: List[ProviderRead] = Field(default_factory=list)
