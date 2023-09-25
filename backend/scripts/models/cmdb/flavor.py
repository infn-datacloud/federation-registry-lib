from typing import List

from app.flavor.schemas import FlavorCreate, FlavorQuery, FlavorRead
from pydantic import UUID4, Field


class FlavorWrite(FlavorCreate):
    name: str = Field(alias="_id")
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this flavor",
    )

    class Config:
        allow_population_by_field_name = True


class FlavorRead(FlavorRead):
    pass


class FlavorQuery(FlavorQuery):
    pass
