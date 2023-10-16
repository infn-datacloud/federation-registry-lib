from typing import Any, Dict, Optional
from uuid import UUID

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import Field, root_validator, validator


class FlavorBase(BaseNode):
    """Model with Flavor basic attributes."""

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

    @validator("uuid", pre=True)
    def to_string(cls, v):
        if isinstance(v, UUID):
            return v.hex
        return v

    @root_validator
    def check_gpu_values(cls, values: Dict[str, Any]):
        if values.get("gpus") == 0:
            assert (
                values.get("gpu_model") is None
            ), "'GPU model' must be None if 'Num GPUs' is 0"
            assert (
                values.get("gpu_vendor") is None
            ), "'GPU vendor' must be None if 'Num GPUs' is 0"
        return values


class FlavorCreate(BaseNodeCreate, FlavorBase):
    """Model to create a Flavor.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.

    Validation: If *num GPUs* is 0, then *gpu model*
    and *gpu vendor* must be none.
    """


class FlavorUpdate(FlavorCreate):
    """Model to update a Flavor.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    name: Optional[str] = Field(
        default=None, description="Flavor name in the provider."
    )
    uuid: Optional[str] = Field(
        default=None, description="Flavor UUID in the provider."
    )


class FlavorRead(BaseNodeRead, FlavorBase):
    """Model, for authenticated users, to read all Flavor data retrieved from
    DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


class FlavorReadPublic(BaseNodeRead, FlavorBase):
    pass


class FlavorReadShort(BaseNodeRead, FlavorBase):
    pass


FlavorQuery = create_query_model("FlavorQuery", FlavorBase)
