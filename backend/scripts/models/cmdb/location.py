from app.location.schemas import LocationCreate, LocationQuery, LocationRead
from pydantic import Field


class LocationWrite(LocationCreate):
    name: str = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True


class LocationRead(LocationRead):
    ...


class LocationQuery(LocationQuery):
    ...
