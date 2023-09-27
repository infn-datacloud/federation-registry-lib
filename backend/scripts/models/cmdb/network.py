from typing import Optional

from app.network.schemas import NetworkCreate, NetworkQuery, NetworkRead
from pydantic import UUID4, Field


class NetworkWrite(NetworkCreate):
    name: str = Field(alias="_id")
    project: Optional[UUID4] = Field(
        default=None,
        description="Project UUIDs which have access to this private network",
    )

    class Config:
        allow_population_by_field_name = True


class NetworkRead(NetworkRead):
    pass


class NetworkQuery(NetworkQuery):
    pass
