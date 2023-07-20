from pydantic import UUID4, BaseModel, Field, root_validator
from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class FlavorBase(BaseModel):
    name: str
    uuid: UUID4
    num_vcpus: int = Field(ge=0, default=0)
    num_gpus: int = Field(ge=0, default=0)
    ram: int = Field(ge=0, default=0)
    disk: int = Field(ge=0, default=0)
    infiniband_support: bool = False
    gpu_model: Optional[str] = None
    gpu_vendor: Optional[str] = None


class FlavorCreate(BaseNodeCreate, FlavorBase):
    """Flavor Create Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PUT or POST request.

    Attributes:
        description (str): Brief description.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): TODO
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
    """

    @root_validator
    def check_gpu_values(cls, values):
        if values.get("num_gpus") == 0:
            if values.get("gpu_model") is not None:
                raise ValueError("'GPU model' must be None if 'Num GPUs' is 0")
            if values.get("gpu_vendor") is not None:
                raise ValueError(
                    "'GPU vendor' must be None if 'Num GPUs' is 0"
                )
        return values


class FlavorUpdate(FlavorCreate):
    """Flavor Update Model class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH request.

    Attributes:
        description (str): Brief description.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): TODO
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
    """


class FlavorRead(BaseNodeRead, FlavorBase):
    """Flavor class.

    Class retrieved from the database.
    Expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Unique ID.
        description (str): Brief description.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): TODO
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
    """


FlavorQuery = create_query_model("FlavorQuery", FlavorBase)
