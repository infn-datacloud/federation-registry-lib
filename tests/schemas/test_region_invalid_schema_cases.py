from typing import Literal

from pytest_cases import case, parametrize

from fed_reg.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    NetworkServiceCreateExtended,
    ObjectStorageServiceCreateExtended,
)
from fed_reg.service.schemas import IdentityServiceCreate


class CaseInvalidAttr:
    @case(tags=["base_public", "base"])
    def case_attr(self) -> tuple[Literal["name"], None]:
        return "name", None

    @case(tags=["create_extended"])
    @parametrize(
        type=(
            "block_storage_services",
            "compute_services",
            "identity_services",
            "network_services",
            "object_storage_services",
        )
    )
    def case_dup_services(
        self,
        block_storage_service_create_ext_schema: BlockStorageServiceCreateExtended,
        compute_service_create_ext_schema: ComputeServiceCreateExtended,
        identity_service_create_schema: IdentityServiceCreate,
        network_service_create_ext_schema: NetworkServiceCreateExtended,
        object_storage_service_create_ext_schema: ObjectStorageServiceCreateExtended,
        type: str,
    ) -> tuple[
        str,
        list[BlockStorageServiceCreateExtended]
        | list[ComputeServiceCreateExtended]
        | list[IdentityServiceCreate]
        | list[NetworkServiceCreateExtended]
        | list[ObjectStorageServiceCreateExtended],
        str,
    ]:
        if type == "block_storage_services":
            service = block_storage_service_create_ext_schema
        elif type == "compute_services":
            service = compute_service_create_ext_schema
        elif type == "identity_services":
            service = identity_service_create_schema
        elif type == "network_services":
            service = network_service_create_ext_schema
        elif type == "object_storage_services":
            service = object_storage_service_create_ext_schema

        return (
            type,
            [service, service],
            "There are multiple items with identical endpoint",
        )
