from typing import List

from app.image.schemas import ImageCreate, ImageQuery, ImageRead
from pydantic import UUID4, Field


class ImageWrite(ImageCreate):
    name: str = Field(alias="_id")
    projects: List[UUID4] = Field(
        default_factory=list,
        description="List of projects UUIDs which have access to this image",
    )

    class Config:
        allow_population_by_field_name = True


class ImageRead(ImageRead):
    pass


class ImageQuery(ImageQuery):
    pass
