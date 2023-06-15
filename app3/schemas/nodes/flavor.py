from pydantic import BaseModel, root_validator
from typing import Optional


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
    num_vcpus: Optional[int] = None
    num_gpus: Optional[int] = None
    ram: Optional[int] = None
    disk: Optional[int] = None
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
    num_vcpus: int = 0
    num_gpus: int = 0
    ram: int = 0
    disk: int = 0
    infiniband_support: bool = False

    @root_validator
    def check_non_negative(cls, values):
        assert values["num_vcpus"] >= 0, "num_vcpus should be non negative"
        assert values["num_gpus"] >= 0, "num_gpus should be non negative"
        assert values["ram"] >= 0, "ram should be non negative"
        assert values["disk"] >= 0, "disk should be non negative"
        return values

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
        if values["num_gpus"] < 1 and (
            values["gpu_model"] is not None or values["gpu_vendor"] is not None
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

    uid: str

    class Config:
        orm_mode = True
