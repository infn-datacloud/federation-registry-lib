from typing import List

from app.provider.schemas_extended import (
    BlockStorageServiceReadExtended,
    ComputeServiceCreateExtended,
    ComputeServiceReadExtended,
    NetworkServiceCreateExtended,
    NetworkServiceReadExtended,
)
from app.service.schemas import (
    BlockStorageServiceCreate,
    BlockStorageServiceQuery,
    ComputeServiceQuery,
    IdentityServiceCreate,
    IdentityServiceQuery,
    IdentityServiceRead,
    NetworkServiceQuery,
)
from models.cmdb.flavor import FlavorWrite
from models.cmdb.image import ImageWrite
from models.cmdb.network import NetworkWrite
from models.cmdb.quota import BlockStorageQuotaWrite, ComputeQuotaWrite
from pydantic import AnyHttpUrl, Field


class ComputeServiceWrite(ComputeServiceCreateExtended):
    endpoint: AnyHttpUrl = Field(alias="_id")
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

    class Config:
        allow_population_by_field_name = True


class BlockStorageServiceWrite(BlockStorageServiceCreate):
    endpoint: AnyHttpUrl = Field(alias="_id")
    quotas: List[BlockStorageQuotaWrite] = Field(
        default_factory=list, description="List of quotas to apply on this service"
    )

    class Config:
        allow_population_by_field_name = True


class NetworkServiceWrite(NetworkServiceCreateExtended):
    endpoint: AnyHttpUrl = Field(alias="_id")
    networks: List[NetworkWrite] = Field(
        default_factory=list,
        description="List of networks accessible through this service",
    )

    class Config:
        allow_population_by_field_name = True


class ComputeServiceRead(ComputeServiceReadExtended):
    ...


class ComputeServiceQuery(ComputeServiceQuery):
    ...


class BlockStorageServiceQuery(BlockStorageServiceQuery):
    ...


class BlockStorageServiceRead(BlockStorageServiceReadExtended):
    ...


class NetworkServiceQuery(NetworkServiceQuery):
    ...


class NetworkServiceRead(NetworkServiceReadExtended):
    ...


class IdentityServiceRead(IdentityServiceRead):
    ...


class IdentityServiceQuery(IdentityServiceQuery):
    ...


class IdentityServiceWrite(IdentityServiceCreate):
    ...
