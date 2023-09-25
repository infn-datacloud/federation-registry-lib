from typing import List

from app.provider.schemas_extended import RegionCreateExtended, RegionReadExtended
from app.region.schemas import RegionQuery
from models.cmdb.service import (
    BlockStorageServiceWrite,
    ComputeServiceWrite,
    NetworkServiceWrite,
)
from pydantic import Field


class RegionWrite(RegionCreateExtended):
    name: str = Field(alias="_id")
    block_storage_services: List[BlockStorageServiceWrite] = Field(
        default_factory=list, description="Block storage service"
    )
    compute_services: List[ComputeServiceWrite] = Field(
        default_factory=list, description="Compute service"
    )
    network_services: List[NetworkServiceWrite] = Field(
        default_factory=list, description="Network service"
    )

    class Config:
        allow_population_by_field_name = True


class RegionRead(RegionReadExtended):
    ...

class RegionQuery(RegionQuery):
    ...
