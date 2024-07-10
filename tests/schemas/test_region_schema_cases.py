from typing import Literal, Optional

from pytest_cases import case, parametrize

from fed_reg.location.schemas import LocationCreate
from fed_reg.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    NetworkServiceCreateExtended,
    ObjectStoreServiceCreateExtended,
)
from fed_reg.service.schemas import IdentityServiceCreate
from tests.utils import random_lower_string, random_url


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["update"])
    def case_attr(self) -> tuple[Literal["name"], None]:
        return "name", None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["create_extended"])
    @parametrize(
        type=[
            "block_storage_services",
            "compute_services",
            "identity_services",
            "network_services",
            "object_store_services",
        ]
    )
    @parametrize(len=(0, 1, 2))
    def case_services(
        self,
        block_storage_service_create_ext_schema: BlockStorageServiceCreateExtended,
        compute_service_create_ext_schema: ComputeServiceCreateExtended,
        identity_service_create_schema: IdentityServiceCreate,
        network_service_create_ext_schema: NetworkServiceCreateExtended,
        object_store_service_create_ext_schema: ObjectStoreServiceCreateExtended,
        type: str,
        len: int,
    ) -> tuple[
        str,
        list[BlockStorageServiceCreateExtended]
        | list[ComputeServiceCreateExtended]
        | list[IdentityServiceCreate]
        | list[NetworkServiceCreateExtended]
        | list[ObjectStoreServiceCreateExtended],
    ]:
        if len > 0:
            if type == "block_storage_services":
                service = block_storage_service_create_ext_schema
            elif type == "compute_services":
                service = compute_service_create_ext_schema
            elif type == "identity_services":
                service = identity_service_create_schema
            elif type == "network_services":
                service = network_service_create_ext_schema
            elif type == "object_store_services":
                service = object_store_service_create_ext_schema

            if len == 1:
                return type, [service]
            elif len == 2:
                service2 = service.copy()
                service2.endpoint = random_url()
                return type, [service, service2]
        else:
            return type, []

    @case(tags=["create_extended"])
    @parametrize(with_loc=[True, False])
    def case_location(
        self, location_create_schema: LocationCreate, with_loc: bool
    ) -> tuple[Literal["location"], Optional[LocationCreate]]:
        if with_loc:
            return "location", location_create_schema
        else:
            return "location", None
