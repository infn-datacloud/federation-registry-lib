from typing import List, Optional

from app.image.enum import ImageOS
from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import UUID4, Field


class ImageBase(BaseNode):
    """Model with Image basic attributes."""

    name: str = Field(description="Image name in the provider.")
    uuid: UUID4 = Field(description="Image UUID in the provider.")
    os_type: Optional[ImageOS] = Field(
        default=None, description="Image Operating System."
    )
    os_distro: Optional[str] = Field(
        default=None, description="Operating system distribution type."
    )
    os_version: Optional[str] = Field(default=None, description="Distribution version.")
    architecture: Optional[str] = Field(
        default=None, description="Operating system architecture."
    )
    kernel_id: Optional[str] = Field(default=None, description="Kernel version")
    cuda_support: bool = Field(default=False, description="Enable CUDA support.")
    gpu_driver: bool = Field(default=False, description="Enable GPU driver support.")
    is_public: bool = Field(default=True, description="Public available")
    tags: List[str] = Field(default_factory=list, description="List of tags")


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
