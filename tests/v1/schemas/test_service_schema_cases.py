from typing import Any, Literal

from pytest_cases import case, parametrize, parametrize_with_cases

from fedreg.service.enum import (
    ServiceType,
)
from fedreg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
    Service,
)
from fedreg.service.schemas import (
    BlockStorageServiceCreate,
    ComputeServiceCreate,
    IdentityServiceCreate,
    NetworkServiceCreate,
    ObjectStoreServiceCreate,
    ServiceBase,
)
from tests.v1.schemas.utils import random_service_name, service_schema_dict
from tests.v1.utils import random_lower_string


class CaseServiceSchema:
    @case(tags=("dict", "valid", "base", "base_public", "update"))
    def case_mandatory(self) -> dict[str, Any]:
        return service_schema_dict()

    @case(tags=("dict", "valid", "base", "base_public", "update"))
    def case_description(self) -> dict[str, Any]:
        return {**service_schema_dict(), "description": random_lower_string()}

    @case(tags=("dict", "valid", "update", "block-storage"))
    def case_mandatory_block_storage(self) -> dict[str, Any]:
        return {**service_schema_dict(ServiceType.BLOCK_STORAGE)}

    @case(tags=("dict", "valid", "update", "block-storage"))
    def case_description_block_storage(self) -> dict[str, Any]:
        return {
            **service_schema_dict(ServiceType.BLOCK_STORAGE),
            "description": random_lower_string(),
        }

    @case(tags=("dict", "valid", "update", "compute"))
    def case_mandatory_compute(self) -> dict[str, Any]:
        return {**service_schema_dict(ServiceType.COMPUTE)}

    @case(tags=("dict", "valid", "update", "compute"))
    def case_description_compute(self) -> dict[str, Any]:
        return {
            **service_schema_dict(ServiceType.COMPUTE),
            "description": random_lower_string(),
        }

    @case(tags=("dict", "valid", "update", "identity"))
    def case_mandatory_identity(self) -> dict[str, Any]:
        return {**service_schema_dict(ServiceType.IDENTITY)}

    @case(tags=("dict", "valid", "update", "identity"))
    def case_description_identity(self) -> dict[str, Any]:
        return {
            **service_schema_dict(ServiceType.IDENTITY),
            "description": random_lower_string(),
        }

    @case(tags=("dict", "valid", "update", "network"))
    def case_mandatory_network(self) -> dict[str, Any]:
        return {**service_schema_dict(ServiceType.NETWORK)}

    @case(tags=("dict", "valid", "update", "network"))
    def case_description_network(self) -> dict[str, Any]:
        return {
            **service_schema_dict(ServiceType.NETWORK),
            "description": random_lower_string(),
        }

    @case(tags=("dict", "valid", "update", "object-store"))
    def case_mandatory_object_store(self) -> dict[str, Any]:
        return {**service_schema_dict(ServiceType.OBJECT_STORE)}

    @case(tags=("dict", "valid", "update", "object-store"))
    def case_description_object_store(self) -> dict[str, Any]:
        return {
            **service_schema_dict(ServiceType.OBJECT_STORE),
            "description": random_lower_string(),
        }

    @case(tags=("dict", "invalid", "base_public", "base", "read_public", "read"))
    def case_missing_endpoint(self) -> tuple[dict[str, Any], Literal["endpoint"]]:
        d = service_schema_dict()
        d.pop("endpoint")
        return d, "endpoint"

    @case(tags=("dict", "invalid", "update", "read"))
    def case_invalid_name(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict()
        d["name"] = random_lower_string()
        return d, "name"

    @case(tags=("dict", "invalid", "block-storage", "read_public", "read"))
    def case_missing_endpoint_block_storage(
        self,
    ) -> tuple[dict[str, Any], Literal["endpoint"]]:
        d = service_schema_dict(ServiceType.BLOCK_STORAGE)
        d.pop("endpoint")
        return d, "endpoint"

    @case(tags=("dict", "invalid", "block-storage"))
    def case_missing_name(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict(ServiceType.BLOCK_STORAGE)
        d.pop("name")
        return d, "name"

    @case(tags=("dict", "invalid", "block-storage", "update"))
    @parametrize(
        service_type=(
            None,
            ServiceType.COMPUTE,
            ServiceType.IDENTITY,
            ServiceType.NETWORK,
            ServiceType.OBJECT_STORE,
        )
    )
    def case_invalid_name_block_storage(
        self, service_type: ServiceType | None
    ) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict()
        if service_type:
            d["name"] = random_service_name(service_type)
        else:
            d["name"] = random_lower_string()
        return d, "name"

    @case(tags=("dict", "invalid", "block-storage", "update"))
    @parametrize(
        value=(
            ServiceType.COMPUTE,
            ServiceType.IDENTITY,
            ServiceType.NETWORK,
            ServiceType.OBJECT_STORE,
        )
    )
    def case_invalid_type_block_storage(
        self, value: ServiceType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = service_schema_dict(ServiceType.BLOCK_STORAGE)
        d["type"] = value
        return d, "type"

    @case(tags=("dict", "invalid", "compute", "read_public", "read"))
    def case_missing_endpoint_compute(
        self,
    ) -> tuple[dict[str, Any], Literal["endpoint"]]:
        d = service_schema_dict(ServiceType.COMPUTE)
        d.pop("endpoint")
        return d, "endpoint"

    @case(tags=("dict", "invalid", "compute"))
    def case_missing_name_compute(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict(ServiceType.COMPUTE)
        d.pop("name")
        return d, "name"

    @case(tags=("dict", "invalid", "compute", "update"))
    @parametrize(
        service_type=(
            None,
            ServiceType.BLOCK_STORAGE,
            ServiceType.IDENTITY,
            ServiceType.NETWORK,
            ServiceType.OBJECT_STORE,
        )
    )
    def case_invalid_name_compute(
        self, service_type: ServiceType | None
    ) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict()
        if service_type:
            d["name"] = random_service_name(service_type)
        else:
            d["name"] = random_lower_string()
        return d, "name"

    @case(tags=("dict", "invalid", "compute", "update"))
    @parametrize(
        value=(
            ServiceType.BLOCK_STORAGE,
            ServiceType.IDENTITY,
            ServiceType.NETWORK,
            ServiceType.OBJECT_STORE,
        )
    )
    def case_invalid_type_compute(
        self, value: ServiceType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = service_schema_dict(ServiceType.COMPUTE)
        d["type"] = value
        return d, "type"

    @case(tags=("dict", "invalid", "identity", "read_public", "read"))
    def case_missing_endpoint_identity(
        self,
    ) -> tuple[dict[str, Any], Literal["endpoint"]]:
        d = service_schema_dict(ServiceType.IDENTITY)
        d.pop("endpoint")
        return d, "endpoint"

    @case(tags=("dict", "invalid", "identity"))
    def case_missing_name_identity(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict(ServiceType.IDENTITY)
        d.pop("name")
        return d, "name"

    @case(tags=("dict", "invalid", "identity", "update"))
    @parametrize(
        service_type=(
            None,
            ServiceType.BLOCK_STORAGE,
            ServiceType.COMPUTE,
            ServiceType.NETWORK,
            ServiceType.OBJECT_STORE,
        )
    )
    def case_invalid_name_identity(
        self, service_type: ServiceType | None
    ) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict()
        if service_type:
            d["name"] = random_service_name(service_type)
        else:
            d["name"] = random_lower_string()
        return d, "name"

    @case(tags=("dict", "invalid", "identity", "update"))
    @parametrize(
        value=(
            ServiceType.BLOCK_STORAGE,
            ServiceType.COMPUTE,
            ServiceType.NETWORK,
            ServiceType.OBJECT_STORE,
        )
    )
    def case_invalid_type_identity(
        self, value: ServiceType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = service_schema_dict(ServiceType.IDENTITY)
        d["type"] = value
        return d, "type"

    @case(tags=("dict", "invalid", "network", "read_public", "read"))
    def case_missing_endpoint_network(
        self,
    ) -> tuple[dict[str, Any], Literal["endpoint"]]:
        d = service_schema_dict(ServiceType.NETWORK)
        d.pop("endpoint")
        return d, "endpoint"

    @case(tags=("dict", "invalid", "network"))
    def case_missing_name_network(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict(ServiceType.NETWORK)
        d.pop("name")
        return d, "name"

    @case(tags=("dict", "invalid", "network", "update"))
    @parametrize(
        service_type=(
            None,
            ServiceType.BLOCK_STORAGE,
            ServiceType.COMPUTE,
            ServiceType.IDENTITY,
            ServiceType.OBJECT_STORE,
        )
    )
    def case_invalid_name_network(
        self, service_type: ServiceType | None
    ) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict()
        if service_type:
            d["name"] = random_service_name(service_type)
        else:
            d["name"] = random_lower_string()
        return d, "name"

    @case(tags=("dict", "invalid", "network", "update"))
    @parametrize(
        value=(
            ServiceType.BLOCK_STORAGE,
            ServiceType.COMPUTE,
            ServiceType.IDENTITY,
            ServiceType.OBJECT_STORE,
        )
    )
    def case_invalid_type_network(
        self, value: ServiceType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = service_schema_dict(ServiceType.NETWORK)
        d["type"] = value
        return d, "type"

    @case(tags=("dict", "invalid", "object-store", "read_public", "read"))
    def case_missing_endpoint_object_store(
        self,
    ) -> tuple[dict[str, Any], Literal["endpoint"]]:
        d = service_schema_dict(ServiceType.OBJECT_STORE)
        d.pop("endpoint")
        return d, "endpoint"

    @case(tags=("dict", "invalid", "object-store"))
    def case_missing_name_object_store(self) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict(ServiceType.OBJECT_STORE)
        d.pop("name")
        return d, "name"

    @case(tags=("dict", "invalid", "object-store", "update"))
    @parametrize(
        service_type=(
            None,
            ServiceType.BLOCK_STORAGE,
            ServiceType.COMPUTE,
            ServiceType.NETWORK,
            ServiceType.IDENTITY,
        )
    )
    def case_invalid_name_object_store(
        self, service_type: ServiceType | None
    ) -> tuple[dict[str, Any], Literal["name"]]:
        d = service_schema_dict()
        if service_type:
            d["name"] = random_service_name(service_type)
        else:
            d["name"] = random_lower_string()
        return d, "name"

    @case(tags=("dict", "invalid", "object-store", "update"))
    @parametrize(
        value=(
            ServiceType.BLOCK_STORAGE,
            ServiceType.COMPUTE,
            ServiceType.IDENTITY,
            ServiceType.NETWORK,
        )
    )
    def case_invalid_type_object_store(
        self, value: ServiceType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = service_schema_dict(ServiceType.OBJECT_STORE)
        d["type"] = value
        return d, "type"


class CaseServiceModel:
    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseServiceSchema, has_tag=("dict", "valid", "base")
    )
    def case_service_model(self, data: dict[str, Any]) -> Service:
        return Service(**ServiceBase(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseServiceSchema, has_tag=("dict", "valid", "block-storage")
    )
    def case_block_storage_service_model(
        self, data: dict[str, Any]
    ) -> BlockStorageService:
        return BlockStorageService(**BlockStorageServiceCreate(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseServiceSchema, has_tag=("dict", "valid", "compute")
    )
    def case_compute_service_model(self, data: dict[str, Any]) -> ComputeService:
        return ComputeService(**ComputeServiceCreate(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseServiceSchema, has_tag=("dict", "valid", "identity")
    )
    def case_identity_service_model(self, data: dict[str, Any]) -> IdentityService:
        return IdentityService(**IdentityServiceCreate(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseServiceSchema, has_tag=("dict", "valid", "network")
    )
    def case_network_service_model(self, data: dict[str, Any]) -> NetworkService:
        return NetworkService(**NetworkServiceCreate(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseServiceSchema, has_tag=("dict", "valid", "object-store")
    )
    def case_object_store_service_model(
        self, data: dict[str, Any]
    ) -> ObjectStoreService:
        return ObjectStoreService(**ObjectStoreServiceCreate(**data).dict()).save()
