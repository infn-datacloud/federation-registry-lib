"""Pydantic models of the Virtual Machine Flavor owned by a Provider."""
from typing import Any, Dict, Optional

from pydantic import Field, root_validator

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model


class FlavorBase(BaseNode):
    """Model with Flavor basic attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Flavor name in the Provider.
        uuid (str): Flavor unique ID in the Provider
        disk (int): Reserved disk size (GiB)
        is_public (bool): Public or private Flavor.
        ram (int): Reserved RAM (MiB)
        vcpus (int): Number of Virtual CPUs.
        swap (int): Swap size (GiB).
        ephemeral (int): Ephemeral disk size (GiB).
        infiniband (bool): MPI - parallel multi-process enabled.
        gpus (int): Number of GPUs.
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
        local_storage (str | None): Local storage presence.
    """

    name: str = Field(description="Flavor name in the provider.")
    uuid: str = Field(description="Flavor UUID in the provider.")
    disk: int = Field(default=0, ge=0, description="Reserved disk size (GB)")
    is_public: bool = Field(default=True, description="Public available")
    ram: int = Field(default=0, ge=0, description="Reserved RAM size (MB)")
    vcpus: int = Field(default=0, ge=0, description="Number of virtual CPUs")
    swap: int = Field(default=0, ge=0, description="Reserved swap disk size (GB)")
    ephemeral: int = Field(
        default=0, ge=0, description="Size of the ephemeral disk (GB)"
    )
    infiniband: bool = Field(
        default=False, description="MPI: parallel multi-process enabled"
    )
    gpus: int = Field(default=0, ge=0, description="Number of GPUs")
    gpu_model: Optional[str] = Field(default=None, description="GPU model name")
    gpu_vendor: Optional[str] = Field(default=None, description="GPU vendor name")
    local_storage: Optional[str] = Field(
        default=None, description="Local storage presence"
    )

    @root_validator
    def check_gpu_values(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """If *num GPUs* is 0, then *gpu model* and *gpu vendor* must be none."""
        if values.get("gpus") == 0:
            assert not values.get(
                "gpu_model"
            ), "'GPU model' must be None if 'Num GPUs' is 0"
            assert not values.get(
                "gpu_vendor"
            ), "'GPU vendor' must be None if 'Num GPUs' is 0"
        return values


class FlavorCreate(BaseNodeCreate, FlavorBase):
    """Model to create a Flavor.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Flavor name in the Provider.
        uuid (str): Flavor unique ID in the Provider
        disk (int): Reserved disk size (GiB)
        is_public (bool): Public or private Flavor.
        ram (int): Reserved RAM (MiB)
        vcpus (int): Number of Virtual CPUs.
        swap (int): Swap size (GiB).
        ephemeral (int): Ephemeral disk size (GiB).
        infiniband (bool): MPI - parallel multi-process enabled.
        gpus (int): Number of GPUs.
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
        local_storage (str | None): Local storage presence.
    """


class FlavorUpdate(BaseNodeCreate, FlavorBase):
    """Model to update a Flavor.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): Flavor name in the Provider.
        uuid (str | None): Flavor unique ID in the Provider
        disk (int | None): Reserved disk size (GiB)
        is_public (bool | None): Public or private Flavor.
        ram (int | None): Reserved RAM (MiB)
        vcpus (int | None): Number of Virtual CPUs.
        swap (int | None): Swap size (GiB).
        ephemeral (int | None): Ephemeral disk size (GiB).
        infiniband (bool | None): MPI - parallel multi-process enabled.
        gpus (int | None): Number of GPUs.
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
        local_storage (str | None): Local storage presence.
    """

    name: Optional[str] = Field(
        default=None, description="Flavor name in the provider."
    )
    uuid: Optional[str] = Field(
        default=None, description="Flavor UUID in the provider."
    )


class FlavorRead(BaseNodeRead, FlavorBase):
    """Model, for authenticated users, to read all Flavor data retrieved from DB.

    Class to read data retrieved from the database. Expected as output when performing a
    generic REST request. It contains all the non- sensible data written in the
    database.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Flavor unique ID.
        description (str): Brief description.
        name (str): Flavor name in the Provider.
        uuid (str): Flavor unique ID in the Provider
        disk (int): Reserved disk size (GiB)
        is_public (bool): Public or private Flavor.
        ram (int): Reserved RAM (MiB)
        vcpus (int): Number of Virtual CPUs.
        swap (int): Swap size (GiB).
        ephemeral (int): Ephemeral disk size (GiB).
        infiniband (bool): MPI - parallel multi-process enabled.
        gpus (int): Number of GPUs.
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
        local_storage (str | None): Local storage presence.
    """


class FlavorReadPublic(BaseNodeRead, FlavorBase):
    pass


class FlavorReadShort(BaseNodeRead, FlavorBase):
    pass


FlavorQuery = create_query_model("FlavorQuery", FlavorBase)
