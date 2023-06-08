from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ImageOS(Enum):
    """Possible Operating system types"""

    Linux: str = "Linux"
    Windows: str = "Windows"
    MacOS: str = "MacOS"


class ImageBase(BaseModel):
    """Image Base class.

    Class without id (which is populated by the database).

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
    os: ImageOS
    distribution: str
    version: str
    architecture: str
    cuda_support: bool = False
    gpu_driver: bool = False
    creation_time: Optional[datetime] = None

    class Config:
        validate_assignment = True


class ImageCreate(ImageBase):
    """Image Create class.

    Class without id (which is populated by the database).
    expected as input when performing a REST request.

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

    pass


class Image(ImageBase):
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

    uid: str

    class Config:
        orm_mode = True
