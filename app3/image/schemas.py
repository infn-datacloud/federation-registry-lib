from datetime import datetime
from typing import Optional

from .enum import ImageOS
from ..models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead


class ImageQuery(BaseNodeQuery):
    """Image Query Model class.

    Attributes:
        description (str | None): Brief description.
        os (str | None): Image Operating System.
        distribution (str | None): OS distribution.
        version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        cuda_support (str | None): Support for cuda enabled.
        gpu_driver (str | None): Support for GPUs.
        creation_time (datetime | None): Image creation time.
    """

    os: Optional[ImageOS] = None
    distribution: Optional[str] = None
    version: Optional[str] = None
    architecture: Optional[str] = None
    cuda_support: Optional[bool] = None
    gpu_driver: Optional[bool] = None
    creation_time: Optional[datetime] = None


class ImagePatch(BaseNodeCreate):
    """Image Patch Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        os (str | None): Image Operating System.
        distribution (str | None): OS distribution.
        version (str | None): Distribution version.
        architecture (str | None): OS architecture.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs.
        creation_time (datetime | None): Image creation time.
    """

    description: str = ""
    os: Optional[ImageOS] = None
    distribution: Optional[str] = None
    version: Optional[str] = None
    architecture: Optional[str] = None
    cuda_support: bool = False
    gpu_driver: bool = False
    creation_time: Optional[datetime] = None


class ImageCreate(ImagePatch):
    """Image Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        os (str): Image Operating System.
        distribution (str): OS distribution.
        version (str): Distribution version.
        architecture (str): OS architecture.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs.
        creation_time (datetime | None): Image creation time.
    """

    os: ImageOS
    distribution: str
    version: str
    architecture: str


class Image(ImageCreate, BaseNodeRead):
    """Image class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        os (str): Image Operating System.
        distribution (str): OS distribution.
        version (str): Distribution version.
        architecture (str): OS architecture.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs.
        creation_time (datetime | None): Image creation time.
    """
