from app.location.schemas import LocationCreate, LocationQuery, LocationRead
from pydantic import BaseModel


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.site}"


class LocationWrite(LocationCreate, Representation):
    pass


class LocationRead(LocationRead, Representation):
    pass


class LocationQuery(LocationQuery, Representation):
    pass
