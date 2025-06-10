from typing import Any, Literal

from pytest_cases import case, parametrize, parametrize_with_cases

from fedreg.v1.quota.enum import QuotaType
from fedreg.v1.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
    Quota,
)
from fedreg.v1.quota.schemas import (
    BlockStorageQuotaCreate,
    ComputeQuotaCreate,
    NetworkQuotaCreate,
    ObjectStoreQuotaCreate,
    QuotaBase,
)
from tests.v1.schemas.utils import quota_schema_dict
from tests.v1.utils import random_int, random_lower_string, random_non_negative_int


class CaseQuotaSchema:
    @case(
        tags=(
            "dict",
            "valid",
            "base",
            "base_public",
            "update",
            "block-storage",
            "compute",
            "network",
            "object-store",
        )
    )
    def case_mandatory(self) -> dict[str, Any]:
        return quota_schema_dict()

    @case(
        tags=(
            "dict",
            "valid",
            "base",
            "base_public",
            "update",
            "block-storage",
            "compute",
            "network",
            "object-store",
        )
    )
    def case_description(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "description": random_lower_string()}

    @case(
        tags=(
            "dict",
            "valid",
            "base",
            "base_public",
            "update",
            "block-storage",
            "compute",
            "network",
            "object-store",
        )
    )
    def case_per_user(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "per_user": True}

    @case(
        tags=(
            "dict",
            "valid",
            "base",
            "base_public",
            "update",
            "block-storage",
            "compute",
            "network",
            "object-store",
        )
    )
    def case_usage(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "usage": True}

    @case(tags=("dict", "valid", "update", "block-storage"))
    @parametrize(value=(-1, "random"))
    def case_gigabytes_block_storage(self, value: int | str) -> dict[str, Any]:
        if value == "random":
            value = random_non_negative_int()
        return {**quota_schema_dict(), "gigabytes": value}

    @case(tags=("dict", "valid", "update", "block-storage"))
    @parametrize(value=(-1, "random"))
    def case_per_volume_gigabytes_block_storage(
        self, value: int | str
    ) -> dict[str, Any]:
        if value == "random":
            value = random_non_negative_int()
        return {**quota_schema_dict(), "per_volume_gigabytes": value}

    @case(tags=("dict", "valid", "update", "block-storage"))
    @parametrize(value=(-1, "random"))
    def case_volumes_block_storage(self, value: int | str) -> dict[str, Any]:
        if value == "random":
            value = random_non_negative_int()
        return {**quota_schema_dict(), "volumes": value}

    @case(tags=("dict", "valid", "update", "compute"))
    def case_cores_compute(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "cores": random_non_negative_int()}

    @case(tags=("dict", "valid", "update", "compute"))
    def case_instances_compute(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "instances": random_non_negative_int()}

    @case(tags=("dict", "valid", "update", "compute"))
    def case_ram_compute(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "ram": random_non_negative_int()}

    @case(tags=("dict", "valid", "update", "network"))
    @parametrize(value=(-1, "random"))
    def case_public_ips_network(self, value: int | str) -> dict[str, Any]:
        if value == "random":
            value = random_non_negative_int()
        return {**quota_schema_dict(), "public_ips": value}

    @case(tags=("dict", "valid", "update", "network"))
    @parametrize(value=(-1, "random"))
    def case_networks_network(self, value: int | str) -> dict[str, Any]:
        if value == "random":
            value = random_non_negative_int()
        return {**quota_schema_dict(), "networks": value}

    @case(tags=("dict", "valid", "update", "network"))
    @parametrize(value=(-1, "random"))
    def case_ports_network(self, value: int | str) -> dict[str, Any]:
        if value == "random":
            value = random_non_negative_int()
        return {**quota_schema_dict(), "ports": value}

    @case(tags=("dict", "valid", "update", "network"))
    @parametrize(value=(-1, "random"))
    def case_security_groups_network(self, value: int | str) -> dict[str, Any]:
        if value == "random":
            value = random_non_negative_int()
        return {**quota_schema_dict(), "security_groups": value}

    @case(tags=("dict", "valid", "update", "network"))
    @parametrize(value=(-1, "random"))
    def case_security_group_rules_network(self, value: int | str) -> dict[str, Any]:
        if value == "random":
            value = random_non_negative_int()
        return {**quota_schema_dict(), "security_group_rules": value}

    @case(tags=("dict", "valid", "update", "object-store"))
    def case_bytes_object_store(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "bytes": random_int(-1, 100)}

    @case(tags=("dict", "valid", "update", "object-store"))
    def case_containers_object_store(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "containers": random_int(-1, 100)}

    @case(tags=("dict", "valid", "update", "object-store"))
    def case_objects_object_store(self) -> dict[str, Any]:
        return {**quota_schema_dict(), "objects": random_int(-1, 100)}

    @case(tags=("dict", "invalid", "block-storage", "update"))
    @parametrize(value=(QuotaType.COMPUTE, QuotaType.NETWORK, QuotaType.OBJECT_STORE))
    def case_invalid_type_block_storage(
        self, value: QuotaType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = quota_schema_dict()
        d["type"] = value
        return d, "type"

    @case(tags=("dict", "invalid", "block-storage", "update"))
    def case_invalid_gigabytes_block_storage(
        self,
    ) -> tuple[dict[str, Any], Literal["gigabytes"]]:
        d = quota_schema_dict()
        d["gigabytes"] = random_int(-100, -2)
        return d, "gigabytes"

    @case(tags=("dict", "invalid", "block-storage", "update"))
    def case_invalid_per_volume_gigabytes_block_storage(
        self,
    ) -> tuple[dict[str, Any], Literal["per_volume_gigabytes"]]:
        d = quota_schema_dict()
        d["per_volume_gigabytes"] = random_int(-100, -2)
        return d, "per_volume_gigabytes"

    @case(tags=("dict", "invalid", "block-storage", "update"))
    def case_invalid_volumes_block_storage(
        self,
    ) -> tuple[dict[str, Any], Literal["volumes"]]:
        d = quota_schema_dict()
        d["volumes"] = random_int(-100, -2)
        return d, "volumes"

    @case(tags=("dict", "invalid", "compute", "update"))
    @parametrize(
        value=(QuotaType.BLOCK_STORAGE, QuotaType.NETWORK, QuotaType.OBJECT_STORE)
    )
    def case_invalid_type_compute(
        self, value: QuotaType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = quota_schema_dict()
        d["type"] = value
        return d, "type"

    @case(tags=("dict", "invalid", "compute", "update"))
    def case_invalid_cores_compute(
        self,
    ) -> tuple[dict[str, Any], Literal["cores"]]:
        d = quota_schema_dict()
        d["cores"] = random_int(-100, -1)
        return d, "cores"

    @case(tags=("dict", "invalid", "compute", "update"))
    def case_invalid_instances_compute(
        self,
    ) -> tuple[dict[str, Any], Literal["instances"]]:
        d = quota_schema_dict()
        d["instances"] = random_int(-100, -1)
        return d, "instances"

    @case(tags=("dict", "invalid", "compute", "update"))
    def case_invalid_ram_compute(
        self,
    ) -> tuple[dict[str, Any], Literal["ram"]]:
        d = quota_schema_dict()
        d["ram"] = random_int(-100, -1)
        return d, "ram"

    @case(tags=("dict", "invalid", "network", "update"))
    @parametrize(
        value=(QuotaType.BLOCK_STORAGE, QuotaType.COMPUTE, QuotaType.OBJECT_STORE)
    )
    def case_invalid_type_network(
        self, value: QuotaType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = quota_schema_dict()
        d["type"] = value
        return d, "type"

    @case(tags=("dict", "invalid", "network", "update"))
    def case_invalid_public_ips_network(
        self,
    ) -> tuple[dict[str, Any], Literal["public_ips"]]:
        d = quota_schema_dict()
        d["public_ips"] = random_int(-100, -2)
        return d, "public_ips"

    @case(tags=("dict", "invalid", "network", "update"))
    def case_invalid_networks_network(
        self,
    ) -> tuple[dict[str, Any], Literal["networks"]]:
        d = quota_schema_dict()
        d["networks"] = random_int(-100, -2)
        return d, "networks"

    @case(tags=("dict", "invalid", "network", "update"))
    def case_invalid_ports_network(
        self,
    ) -> tuple[dict[str, Any], Literal["ports"]]:
        d = quota_schema_dict()
        d["ports"] = random_int(-100, -2)
        return d, "ports"

    @case(tags=("dict", "invalid", "network", "update"))
    def case_invalid_security_groups_network(
        self,
    ) -> tuple[dict[str, Any], Literal["security_groups"]]:
        d = quota_schema_dict()
        d["security_groups"] = random_int(-100, -2)
        return d, "security_groups"

    @case(tags=("dict", "invalid", "network", "update"))
    def case_invalid_security_group_rules_network(
        self,
    ) -> tuple[dict[str, Any], Literal["security_group_rules"]]:
        d = quota_schema_dict()
        d["security_group_rules"] = random_int(-100, -2)
        return d, "security_group_rules"

    @case(tags=("dict", "invalid", "object-store", "update"))
    @parametrize(value=(QuotaType.BLOCK_STORAGE, QuotaType.COMPUTE, QuotaType.NETWORK))
    def case_invalid_type_object_store(
        self, value: QuotaType
    ) -> tuple[dict[str, Any], Literal["type"]]:
        d = quota_schema_dict()
        d["type"] = value
        return d, "type"

    @case(tags=("dict", "invalid", "object-store", "update"))
    def case_invalid_bytes_object_store(
        self,
    ) -> tuple[dict[str, Any], Literal["bytes"]]:
        d = quota_schema_dict()
        d["bytes"] = random_int(-100, -2)
        return d, "bytes"

    @case(tags=("dict", "invalid", "object-store", "update"))
    def case_invalid_containers_object_store(
        self,
    ) -> tuple[dict[str, Any], Literal["containers"]]:
        d = quota_schema_dict()
        d["containers"] = random_int(-100, -2)
        return d, "containers"

    @case(tags=("dict", "invalid", "object-store", "update"))
    def case_invalid_objects_object_store(
        self,
    ) -> tuple[dict[str, Any], Literal["objects"]]:
        d = quota_schema_dict()
        d["objects"] = random_int(-100, -2)
        return d, "objects"


class CaseQuotaModel:
    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseQuotaSchema, has_tag=("dict", "valid", "base")
    )
    def case_quota_model(self, data: dict[str, Any]) -> Quota:
        return Quota(**QuotaBase(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseQuotaSchema, has_tag=("dict", "valid", "block-storage")
    )
    def case_block_storage_quota_model(self, data: dict[str, Any]) -> BlockStorageQuota:
        return BlockStorageQuota(**BlockStorageQuotaCreate(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseQuotaSchema, has_tag=("dict", "valid", "compute")
    )
    def case_compute_quota_model(self, data: dict[str, Any]) -> ComputeQuota:
        return ComputeQuota(**ComputeQuotaCreate(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseQuotaSchema, has_tag=("dict", "valid", "network")
    )
    def case_network_quota_model(self, data: dict[str, Any]) -> NetworkQuota:
        return NetworkQuota(**NetworkQuotaCreate(**data).dict()).save()

    @case(tags="model")
    @parametrize_with_cases(
        "data", cases=CaseQuotaSchema, has_tag=("dict", "valid", "object-store")
    )
    def case_object_store_quota_model(self, data: dict[str, Any]) -> ObjectStoreQuota:
        return ObjectStoreQuota(**ObjectStoreQuotaCreate(**data).dict()).save()
