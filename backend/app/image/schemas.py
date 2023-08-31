from datetime import datetime
from typing import Optional

from app.image.enum import ImageOS
from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import UUID4, BaseModel, Field


class ImageBase(BaseModel):
    """Model with Image basic attributes."""

    name: str = Field(description="Image name in the provider.")
    uuid: UUID4 = Field(description="Image UUID in the provider.")
    os: ImageOS = Field(description="Image Operating System.")
    distribution: str = Field(description="Operating system distribution type.")
    version: str = Field(description="Distribution version.")
    architecture: str = Field(description="Operating system architecture.")
    cuda_support: bool = Field(default=False, description="Enable CUDA support.")
    gpu_driver: bool = Field(default=False, description="Enable GPU driver support.")
    creation_time: Optional[datetime] = Field(
        default=None, description="Image creation time."
    )


class ImageCreate(BaseNodeCreate, ImageBase):
    """Model to create an Image.

    Class without id (which is populated by the database). Expected as
    input when performing a POST request.
    """


class ImageUpdate(ImageCreate):
    """Model to update an Image.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    name: Optional[str] = Field(default=None, description="Image name in the provider.")
    uuid: Optional[UUID4] = Field(
        default=None, description="Image UUID in the provider."
    )
    os: Optional[ImageOS] = Field(default=None, description="Image Operating System.")
    distribution: Optional[str] = Field(
        default=None, description="Operating system distribution type."
    )
    version: Optional[str] = Field(default=None, description="Distribution version.")
    architecture: Optional[str] = Field(
        default=None, description="Operating system architecture."
    )


class ImageRead(BaseNodeRead, ImageBase):
    """Model to read Image data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class ImageReadPublic(BaseNodeRead, ImageBase):
    pass


class ImageReadShort(BaseNodeRead, ImageBase):
    pass


ImageQuery = create_query_model("ImageQuery", ImageBase)
