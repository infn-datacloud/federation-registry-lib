from typing import List

from app.provider.schemas_extended import RegionCreateExtended
from models.cmdb.service import BlockStorageServiceWrite, ComputeServiceWrite
from pydantic import Field


class RegionWrite(RegionCreateExtended):
    block_storage_services: List[BlockStorageServiceWrite] = Field(
        default_factory=list, description="Block storage service"
    )
    compute_services: List[ComputeServiceWrite] = Field(
        default_factory=list, description="Compute service"
    )
    # identity_services: List[IdentityServiceCreate] = Field(
    #    default_factory=list, description="Identity service"
    # )
    # network_services: List[NetworkServiceCreateExtended] = Field(
    #    default_factory=list, description="Network service"
    # )
