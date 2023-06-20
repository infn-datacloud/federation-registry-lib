from pydantic import BaseModel, Field, root_validator
from typing import Optional
from uuid import UUID


class FlavorBase(BaseModel):
    """Flavor Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

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

    description: Optional[str] = None
    num_vcpus: Optional[int] = Field(ge=0, default=None)
    num_gpus: Optional[int] = Field(ge=0, default=None)
    ram: Optional[int] = Field(ge=0, default=None)
    disk: Optional[int] = Field(ge=0, default=None)
    infiniband_support: Optional[bool] = None
    gpu_model: Optional[str] = None
    gpu_vendor: Optional[str] = None

    class Config:
        validate_assignment = True


class FlavorUpdate(FlavorBase):
    """Flavor Base class.

    Class without id (which is populated by the database).
    Expected as input when performing a PATCH REST request.

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

    description: str = ""
    num_vcpus: int = Field(ge=0, default=0)
    num_gpus: int = Field(ge=0, default=0)
    ram: int = Field(ge=0, default=0)
    disk: int = Field(ge=0, default=0)
    infiniband_support: bool = False

    class Config:
        validate_assignment = True


class FlavorCreate(FlavorUpdate):
    """Flavor Create class.

    Class without id (which is populated by the database).
    Expected as input when performing a POST REST request.

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

    @root_validator(pre=True)
    def check_gpu_values(cls, values):
        if values.get("num_gpus", 0) < 1 and (
            values.get("gpu_model") is not None
            or values.get("gpu_vendor") is not None
        ):
            raise ValueError(
                "GPU model and GPU vendor should be None if NUM GPUs is 0"
            )
        return values


class Flavor(FlavorCreate):
    """Flavor class.

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Flavor unique ID.
        description (str): Brief description.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): TODO
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
    """

    uid: UUID

    class Config:
        orm_mode = True
