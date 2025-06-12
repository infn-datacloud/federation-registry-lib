"""Pydantic models of the Virtual Machine StorageClass owned by a Provider."""

from pydantic.v1 import Field

from fedreg.v1.core import (
    BaseNode,
    BaseNodeCreate,
    BaseNodeRead,
    BaseReadPrivate,
    BaseReadPublic,
    create_query_model,
)


class StorageClassBasePublic(BaseNode):
    """Model with StorageClass public attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): StorageClass name in the Resource Provider.
        uuid (str): StorageClass unique ID in the Resource Provider.
    """

    name: str = Field(description="StorageClass name")


class StorageClassBase(StorageClassBasePublic):
    """Model with StorageClass public and restricted attributes.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): StorageClass name in the Resource Provider.
        uuid (str): StorageClass unique ID in the Resource Provider.
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

    is_default: bool = Field(
        default=False, description="StorageClass is the cluster default one"
    )
    provisioner: str = Field(
        description="A provisioner determines what volume plugin is used for "
        "provisioning PVs"
    )


class StorageClassCreate(BaseNodeCreate, StorageClassBase):
    """Model to create a StorageClass.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.

    Attributes:
    ----------
        description (str): Brief description.
        name (str): StorageClass name in the Resource Provider.
        uuid (str): StorageClass unique ID in the Resource Provider.
        disk (int): Reserved disk size (GiB)
        is_shared (bool): Public or private StorageClass.
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


class StorageClassUpdate(BaseNodeCreate, StorageClassBase):
    """Model to update a StorageClass.

    Class without id (which is populated by the database). Expected as input when
    performing a PUT request.

    Default to None attributes with a different default or required.

    Attributes:
    ----------
        description (str | None): Brief description.
        name (str | None): StorageClass name in the Resource Provider.
        uuid (str | None): StorageClass unique ID in the Resource Provider.
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

    name: str | None = Field(
        default=None, description="StorageClass is the cluster default one"
    )
    is_default: bool | None = Field(
        default=None, description="StorageClass is the cluster default one"
    )
    provisioner: str | None = Field(
        default=None,
        description="A provisioner determines what volume plugin is used for "
        "provisioning PVs",
    )


class StorageClassReadPublic(BaseNodeRead, BaseReadPublic, StorageClassBasePublic):
    """Model, for non-authenticated users, to read StorageClass data from DB.

    Class to read non-sensible data written in the DB. Expected as output when
    performing a generic REST request without authentication.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): StorageClass unique ID.
        description (str): Brief description.
        name (str): StorageClass name in the Resource Provider.
        uuid (str): StorageClass unique ID in the Resource Provider.
    """


class StorageClassRead(BaseNodeRead, BaseReadPrivate, StorageClassBase):
    """Model, for authenticated users, to read StorageClass data from DB.

    Class to read all data written in the DB. Expected as output when performing a
    generic REST request with an authenticated user.

    Add the *uid* attribute, which is the item unique identifier in the database.

    Attributes:
    ----------
        uid (str): StorageClass unique ID.
        description (str): Brief description.
        name (str): StorageClass name in the Resource Provider.
        uuid (str): StorageClass unique ID in the Resource Provider.
        disk (int): Reserved disk size (GiB)
        is_shared (bool): Public or private StorageClass.
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


StorageClassQuery = create_query_model("StorageClassQuery", StorageClassBase)
