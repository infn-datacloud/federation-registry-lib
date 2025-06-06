"""Pydantic models of the Virtual Machine Flavor owned by a Provider."""

from typing import Annotated, Any

from pydantic import BaseModel, Field, validator

from fedreg.core import BaseNode, BaseNodeRead


class FlavorBase(BaseNode):
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

    name: Annotated[str, Field(description="Flavor name in the Resource Provider.")]
    uuid: Annotated[
        str, Field(description="Flavor unique ID in the Resource Provider.")
    ]
    disk: Annotated[
        int, Field(default=0, ge=0, description="Reserved disk size (GiB).")
    ]
    ram: Annotated[int, Field(default=0, ge=0, description="Reserved RAM (MiB).")]
    vcpus: Annotated[int, Field(default=0, ge=0, description="Number of Virtual CPUs.")]
    swap: Annotated[int, Field(default=0, ge=0, description="Swap size (GiB).")]
    ephemeral: Annotated[
        int, Field(default=0, ge=0, description="Ephemeral disk size (GiB).")
    ]
    infiniband: Annotated[
        bool, Field(default=False, description="MPI - parallel multi-process enabled.")
    ]
    gpu_model: Annotated[str | None, Field(default=None, description="GPU model name.")]
    gpu_vendor: Annotated[
        str | None, Field(default=None, description="Name of the GPU vendor.")
    ]
    gpus: Annotated[int, Field(default=0, ge=0, description="Local storage presence.")]
    local_storage: Annotated[
        str | None, Field(default=None, description="Local storage presence.")
    ]


class FlavorCreate(FlavorBase):
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


class FlavorRead(BaseNodeRead, FlavorBase):
    """Model, for authenticated users, to read Flavor data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *id* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        id (str): Flavor unique ID.
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


class FlavorQuery(BaseModel):
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

    name: Annotated[
        str | None,
        Field(default=None, description="Flavor name in the Resource Provider."),
    ]
    uuid: Annotated[
        str | None,
        Field(default=None, description="Flavor unique ID in the Resource Provider."),
    ]
    disk: Annotated[
        int | None, Field(default=None, description="Reserved disk size (GiB).")
    ]
    ram: Annotated[int | None, Field(default=None, description="Reserved RAM (MiB).")]
    vcpus: Annotated[
        int | None, Field(default=None, description="Number of Virtual CPUs.")
    ]
    swap: Annotated[int | None, Field(default=None, description="Swap size (GiB).")]
    ephemeral: Annotated[
        int | None, Field(default=None, description="Ephemeral disk size (GiB).")
    ]
    infiniband: Annotated[
        bool | None,
        Field(default=None, description="MPI - parallel multi-process enabled."),
    ]
    gpu_model: Annotated[str | None, Field(default=None, description="GPU model name.")]
    gpu_vendor: Annotated[
        str | None, Field(default=None, description="Name of the GPU vendor.")
    ]
    gpus: Annotated[
        int | None, Field(default=None, description="Local storage presence.")
    ]
    local_storage: Annotated[
        str | None, Field(default=None, description="Local storage presence.")
    ]
