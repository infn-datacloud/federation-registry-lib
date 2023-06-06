from uuid import UUID
from pydantic import BaseModel


class FlavorBase(BaseModel):
    """Flavor Base class.

    Class without id which is populated by the database.

    Attributes:
        name (str): Flavor name.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): #TODO: What is it?
    """

    name: str
    num_vcpus: int = 0
    num_gpus: int = 0
    ram: int = 0
    disk: int = 0
    infiniband_support: bool = False

    class Config:
        validate_assignment = True


class FlavorCreate(FlavorBase):
    """Flavor Base class.

    Class without id which is populated by the database.

    Attributes:
        name (str): Flavor name.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): #TODO: What is it?
    """

    pass


class Flavor(FlavorBase):
    """Flavor Base class.

    Class without id which is populated by the database.

    Attributes:
        id (int): Flavor unique ID.
        name (str): Flavor name.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): #TODO: What is it?
        project_id (int): ID of the project
    """

    id: UUID
    project_id: UUID

    class Config:
        orm_mode = True
