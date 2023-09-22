from typing import List

from app.provider.schemas_extended import (
    ComputeServiceCreateExtended,
    NetworkServiceCreateExtended,
    IdentityServiceCreate as IdentityServiceWrite,
)
from app.service.schemas import BlockStorageServiceCreate
from models.cmdb.flavor import FlavorWrite
from models.cmdb.image import ImageWrite
from models.cmdb.network import NetworkWrite
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from pydantic import Field


class ComputeServiceWrite(ComputeServiceCreateExtended):
    flavors: List[FlavorWrite] = Field(
        default_factory=list,
        description="List of flavors accessible through this service",
    )
    images: List[ImageWrite] = Field(
        default_factory=list,
        description="List of images accessible through this service",
    )
    quotas: List[ComputeQuotaWrite] = Field(
        default_factory=list, description="List of quotas to apply on this service"
    )


class BlockStorageServiceWrite(BlockStorageServiceCreate):
    quotas: List[BlockStorageQuotaWrite] = Field(
        default_factory=list, description="List of quotas to apply on this service"
    )


class NetworkServiceWrite(NetworkServiceCreateExtended):
    networks: List[NetworkWrite] = Field(
        default_factory=list,
        description="List of networks accessible through this service",
    )
