from typing import Optional

from app.models import BaseNodeCreate, BaseNodeRead
from app.query import create_query_model
from pydantic import UUID4, BaseModel, Field, root_validator


class FlavorBase(BaseModel):
    """Model with Flavor basic attributes."""

    name: str = Field(description="Flavor name in the provider.")
    uuid: UUID4 = Field(description="Flavor UUID in the provider.")
    vcpus: int = Field(default=0, ge=0, description="Number of virtual CPUs")
    ram: int = Field(default=0, ge=0, description="Reserved RAM size (MB)")
    disk: int = Field(default=0, ge=0, description="Reserved disk size (GB)")
    swap: int = Field(
        default=0, ge=0, description="Reserved swap disk size (GB)"
    )
    infiniband_support: bool = Field(default=False, description="")  # TODO
    num_gpus: int = Field(default=0, ge=0, description="Number of GPUs")
    gpu_model: Optional[str] = Field(
        default=None, description="GPU model name"
    )
    gpu_vendor: Optional[str] = Field(
        default=None, description="GPU vendor name"
    )


class FlavorCreate(BaseNodeCreate, FlavorBase):
    """Model to create a Flavor.

    Class without id (which is populated by the database).
    Expected as input when performing a POST request.

    Validation: If *num GPUs* is 0, then *gpu model*
    and *gpu vendor* must be none.
    """

    @root_validator
    def check_gpu_values(cls, values):
        if values.get("num_gpus") == 0:
            if values.get("gpu_model") is not None:
                raise ValueError("'GPU model' must be None if 'Num GPUs' is 0")
            if values.get("gpu_vendor") is not None:
                raise ValueError(
                    "'GPU vendor' must be None if 'Num GPUs' is 0"
                )
        return values


class FlavorUpdate(FlavorCreate):
    """Model to update a Flavor.

    Class without id (which is populated by the database). Expected as
    input when performing a PUT request.

    Default to None mandatory attributes.
    """

    name: Optional[str] = Field(
        default=None, description="Flavor name in the provider."
    )
    uuid: Optional[UUID4] = Field(
        default=None, description="Flavor UUID in the provider."
    )


class FlavorRead(BaseNodeRead, FlavorBase):
    """Model to read Flavor data retrieved from DB.

    Class to read data retrieved from the database. Expected as output
    when performing a generic REST request. It contains all the non-
    sensible data written in the database.

    Add the *uid* attribute, which is the item unique identifier in the
    database.
    """


FlavorQuery = create_query_model("FlavorQuery", FlavorBase)
