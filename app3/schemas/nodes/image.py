from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from ..utils import ImageOS


class ImageBase(BaseModel):
    """Image Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        description (str): Brief description.
        os (str): Image Operating System.
        distribution (str): OS distribution.
        version (str): Distribution version.
        architecture (str): OS architecture.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs.
        creation_time (datetime): Image creation time.
    """

    description: Optional[str] = None
    os: Optional[ImageOS] = None
    distribution: Optional[str] = None
    version: Optional[str] = None
    architecture: Optional[str] = None
    cuda_support: bool = False
    gpu_driver: bool = False
    creation_time: Optional[datetime] = None

    class Config:
        validate_assignment = True


class ImageUpdate(ImageBase):
    """Image Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

    Attributes:
        description (str): Brief description.
        os (str): Image Operating System.
        distribution (str): OS distribution.
        version (str): Distribution version.
        architecture (str): OS architecture.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs.
        creation_time (datetime): Image creation time.
    """

    description: str = ""


class ImageCreate(ImageUpdate):
    """Image Create class.

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

    Attributes:
        description (str): Brief description.
        os (str): Image Operating System.
        distribution (str): OS distribution.
        version (str): Distribution version.
        architecture (str): OS architecture.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs.
        creation_time (datetime): Image creation time.
    """

    os: ImageOS
    distribution: str
    version: str
    architecture: str


class Image(ImageCreate):
    """Image Base class.

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Image unique ID.
        description (str): Brief description.
        os (str): Image Operating System.
        distribution (str): OS distribution.
        version (str): Distribution version.
        architecture (str): OS architecture.
        cuda_support (str): Support for cuda enabled.
        gpu_driver (str): Support for GPUs.
        creation_time (datetime): Image creation time.
    """

    uid: UUID

    class Config:
        orm_mode = True
