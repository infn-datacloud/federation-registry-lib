from pydantic import BaseModel
from typing import Optional


class FlavorBase(BaseModel):
    """Flavor Base class.

    Class without id (which is populated by the database).

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
    num_vcpus: int = 0
    num_gpus: int = 0
    ram: int = 0
    disk: int = 0
    infiniband_support: bool = False
    gpu_model: Optional[str] = None
    gpu_vendor: Optional[str] = None

    class Config:
        validate_assignment = True


class FlavorCreate(FlavorBase):
    """Flavor Create class.

    Class without id (which is populated by the database).
    expected as input when performing a REST request.

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

    pass


class Flavor(FlavorBase):
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

    uid: str

    class Config:
        orm_mode = True
