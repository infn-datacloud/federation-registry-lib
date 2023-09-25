from typing import List

from app.network.schemas import NetworkCreate, NetworkQuery, NetworkRead
from pydantic import UUID4, Field


class NetworkWrite(NetworkCreate):
    name: str = Field(alias="_id")
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this network",
    )

    class Config:
        allow_population_by_field_name = True


class NetworkRead(NetworkRead):
    pass


class NetworkQuery(NetworkQuery):
    pass
