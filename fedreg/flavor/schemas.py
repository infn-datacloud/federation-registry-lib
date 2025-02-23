"""Pydantic models of the Virtual Machine Flavor owned by a Provider."""

from typing import Any, Literal

from pydantic import Field, validator

from fedreg.core import (
    BaseNode,
    BaseNodeCreate,
    BaseNodeRead,
    BaseReadPrivate,
    BaseReadPublic,
    create_query_model,
)
from fedreg.flavor.constants import (
    DOC_DISK,
    DOC_EPHEM,
    DOC_GPU_MOD,
    DOC_GPU_VND,
    DOC_GPUS,
    DOC_INFI,
    DOC_LOC_STO,
    DOC_NAME,
    DOC_RAM,
    DOC_SHARED,
    DOC_SWAP,
    DOC_UUID,
    DOC_VCPUS,
)


class FlavorBasePublic(BaseNode):
    """Model with Flavor public attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        uuid (str): Flavor unique ID in the Resource Provider.
    """

    name: str = Field(description=DOC_NAME)
    uuid: str = Field(description=DOC_UUID)


class FlavorBase(FlavorBasePublic):
    """Model with Flavor public and restricted attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        uuid (str): Flavor unique ID in the Resource Provider.
        disk (int): Reserved disk size (GiB).
        ram (int): Reserved RAM (MiB).
        vcpus (int): Number of Virtual CPUs.
        swap (int): Swap size (GiB).
        ephemeral (int): Ephemeral disk size (GiB).
        infiniband (bool): MPI - parallel multi-process enabled.
        gpus (int): Number of GPUs.
        gpu_model (str | None): GPU model name.
        gpu_vendor (str | None): Name of the GPU vendor.
        local_storage (str | None): Local storage presence.
    """

    disk: int = Field(default=0, ge=0, description=DOC_DISK)
    ram: int = Field(default=0, ge=0, description=DOC_RAM)
    vcpus: int = Field(default=0, ge=0, description=DOC_VCPUS)
    swap: int = Field(default=0, ge=0, description=DOC_SWAP)
    ephemeral: int = Field(default=0, ge=0, description=DOC_EPHEM)
    infiniband: bool = Field(default=False, description=DOC_INFI)
    gpu_model: str | None = Field(default=None, description=DOC_GPU_MOD)
    gpu_vendor: str | None = Field(default=None, description=DOC_GPU_VND)
    gpus: int = Field(default=0, ge=0, description=DOC_GPUS)
    local_storage: str | None = Field(default=None, description=DOC_LOC_STO)

    @validator("gpus")
    @classmethod
    def check_gpu_values(cls, v: int, values: dict[str, Any]) -> dict[str, Any]:
        """If *num GPUs* is 0, then *gpu model* and *gpu vendor* must be none."""
        if v == 0:
            assert not values.get("gpu_model", None), (
                "'GPU model' must be None if 'Num GPUs' is 0"
            )
            assert not values.get("gpu_vendor", None), (
                "'GPU vendor' must be None if 'Num GPUs' is 0"
            )
        return v


class PrivateFlavorCreate(BaseNodeCreate, FlavorBase):
    """Model to create a Flavor.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        uuid (str): Flavor unique ID in the Resource Provider.
        disk (int): Reserved disk size (GiB)
        is_shared (bool): Public or private Flavor.
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

    is_shared: Literal[False] = Field(default=False, description=DOC_SHARED)


class SharedFlavorCreate(BaseNodeCreate, FlavorBase):
    """Model to create a Flavor.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        uuid (str): Flavor unique ID in the Resource Provider.
        disk (int): Reserved disk size (GiB)
        is_shared (bool): Public or private Flavor.
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

    is_shared: Literal[True] = Field(default=True, description=DOC_SHARED)


class FlavorUpdate(BaseNodeCreate, FlavorBase):
    """Model to update a Flavor.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): Flavor name in the Resource Provider.
        uuid (str | None): Flavor unique ID in the Resource Provider.
        disk (int | None): Reserved disk size (GiB)
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

    name: str | None = Field(default=None, description=DOC_NAME)
    uuid: str | None = Field(default=None, description=DOC_UUID)


class FlavorReadPublic(BaseNodeRead, BaseReadPublic, FlavorBasePublic):
    """Model, for non-authenticated users, to read Flavor data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Flavor unique ID.
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        uuid (str): Flavor unique ID in the Resource Provider.
    """


class FlavorRead(BaseNodeRead, BaseReadPrivate, FlavorBase):
    """Model, for authenticated users, to read Flavor data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): Flavor unique ID.
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        uuid (str): Flavor unique ID in the Resource Provider.
        disk (int): Reserved disk size (GiB)
        is_shared (bool): Public or private Flavor.
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

    is_shared: bool | None = Field(default=None, description=DOC_SHARED)


FlavorQuery = create_query_model("FlavorQuery", FlavorBase)
