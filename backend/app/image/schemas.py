from datetime import datetime
from pydantic import UUID4, BaseModel
from typing import Optional

from app.image.enum import ImageOS
from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class ImageBase(BaseModel):
    name: str
    uuid: UUID4
    os: ImageOS
    distribution: str
    version: str
    architecture: str
    cuda_support: bool = False
    gpu_driver: bool = False
    creation_time: Optional[datetime] = None


class ImageCreate(BaseNodeCreate, ImageBase):
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


class ImageUpdate(ImageCreate):
    """Image Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT request.

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


class ImageRead(BaseNodeRead, ImageBase):
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


ImageQuery = create_query_model("ImageQuery", ImageBase)
