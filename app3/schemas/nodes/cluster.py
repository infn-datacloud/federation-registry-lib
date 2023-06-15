from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ClusterBase(BaseModel):
    """Cluster Base class.

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

    class Config:
        validate_assignment = True


class ClusterUpdate(ClusterBase):
    """Cluster Base class.

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


class ClusterCreate(ClusterUpdate):
    """Cluster Create class.

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

    pass


class Cluster(ClusterCreate):
    """Cluster class.

    Class retrieved from the database
    expected as output when performing a REST request.
    It contains all the non-sensible data written
    in the database.

    Attributes:
        uid (uuid): Cluster unique ID.
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
