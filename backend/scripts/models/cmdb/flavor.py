from typing import List

from app.flavor.schemas import FlavorCreate, FlavorQuery, FlavorRead
from pydantic import UUID4, BaseModel, Field


class Representation(BaseModel):
    def __str__(self) -> str:
        return f"{self.name}"


class FlavorWrite(FlavorCreate, Representation):
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this flavor",
    )


class FlavorRead(FlavorRead, Representation):
    pass


class FlavorQuery(FlavorQuery, Representation):
    pass
