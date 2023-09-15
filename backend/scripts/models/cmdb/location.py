from app.location.schemas import LocationCreate, LocationQuery, LocationRead
from pydantic import BaseModel


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.name}"


class LocationWrite(LocationCreate, Representation):
    pass


class LocationRead(LocationRead, Representation):
    pass


class LocationQuery(LocationQuery, Representation):
    pass
