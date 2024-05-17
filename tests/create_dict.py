from typing import Any
from uuid import uuid4

from fed_reg.quota.enum import QuotaType
from fed_reg.service.enum import (
    BlockStorageServiceName,
    ComputeServiceName,
    IdentityServiceName,
    NetworkServiceName,
    ObjectStorageServiceName,
    ServiceType,
)
from tests.utils import (
    random_country,
    random_lower_string,
    random_provider_type,
    random_service_name,
    random_start_end_dates,
    random_url,
)


def auth_method_dict() -> dict[str, str]:
    return {"idp_name": random_lower_string(), "protocol": random_lower_string()}


def flavor_model_dict() -> dict[str, str]:
    d = flavor_schema_dict()
    d["uuid"] = d["uuid"].hex
    return d


def flavor_schema_dict() -> dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def identity_provider_model_dict() -> dict[str, str]:
    return identity_provider_schema_dict()


def identity_provider_schema_dict() -> dict[str, str]:
    return {"endpoint": random_url(), "group_claim": random_lower_string()}


def image_model_dict() -> dict[str, str]:
    d = image_schema_dict()
    d["uuid"] = d["uuid"].hex
    return d


def image_schema_dict() -> dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def location_model_dict() -> dict[str, str]:
    return {"site": random_lower_string(), "country": random_country()}


def location_schema_dict() -> dict[str, str]:
    return location_model_dict()


def network_model_dict() -> dict[str, str]:
    d = network_schema_dict()
    d["uuid"] = d["uuid"].hex
    return d


def network_schema_dict() -> dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def project_model_dict() -> dict[str, str]:
    d = project_schema_dict()
    d["uuid"] = d["uuid"].hex
    return d


def project_schema_dict() -> dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def provider_model_dict() -> dict[str, str]:
    d = provider_schema_dict()
    d["type"] = d["type"].value
    return d


def provider_schema_dict() -> dict[str, str]:
    return {"name": random_lower_string(), "type": random_provider_type()}


def quota_model_dict() -> dict[str, str]:
    return {"type": random_lower_string()}


def block_storage_quota_model_dict() -> dict[str, str]:
    return {"type": QuotaType.BLOCK_STORAGE.value}


def compute_quota_model_dict() -> dict[str, str]:
    return {"type": QuotaType.COMPUTE.value}


def network_quota_model_dict() -> dict[str, str]:
    return {"type": QuotaType.NETWORK.value}


def object_storage_quota_model_dict() -> dict[str, str]:
    return {"type": QuotaType.OBJECT_STORAGE.value}


def region_model_dict() -> dict[str, str]:
    return region_schema_dict()


def region_schema_dict() -> dict[str, str]:
    return {"name": random_lower_string()}


def service_model_dict() -> dict[str, str]:
    return {
        "type": random_lower_string(),
        "endpoint": random_lower_string(),
        "name": random_lower_string(),
    }


def service_schema_dict() -> dict[str, str]:
    return {"endpoint": random_url()}


def block_storage_service_model_dict() -> dict[str, str]:
    d = block_storage_service_schema_dict()
    d["name"] = d["name"].value
    d["type"] = ServiceType.BLOCK_STORAGE.value
    return d


def block_storage_service_schema_dict() -> dict[str, str]:
    d = service_schema_dict()
    d["name"] = random_service_name(BlockStorageServiceName)
    return d


def compute_service_model_dict() -> dict[str, str]:
    d = compute_service_schema_dict()
    d["name"] = d["name"].value
    d["type"] = ServiceType.COMPUTE.value
    return d


def compute_service_schema_dict() -> dict[str, str]:
    d = service_schema_dict()
    d["name"] = random_service_name(ComputeServiceName)
    return d


def identity_service_model_dict() -> dict[str, str]:
    d = identity_service_schema_dict()
    d["name"] = d["name"].value
    d["type"] = ServiceType.IDENTITY.value
    return d


def identity_service_schema_dict() -> dict[str, str]:
    d = service_schema_dict()
    d["name"] = random_service_name(IdentityServiceName)
    return d


def network_service_model_dict() -> dict[str, str]:
    d = network_service_schema_dict()
    d["name"] = d["name"].value
    d["type"] = ServiceType.NETWORK.value
    return d


def network_service_schema_dict() -> dict[str, str]:
    d = service_schema_dict()
    d["name"] = random_service_name(NetworkServiceName)
    return d

def object_storage_service_model_dict() -> dict[str, str]:
    d = object_storage_service_schema_dict()
    d["name"] = d["name"].value
    d["type"] = ServiceType.OBJECT_STORAGE.value
    return d


def object_storage_service_schema_dict() -> dict[str, str]:
    d = service_schema_dict()
    d["name"] = random_service_name(ObjectStorageServiceName)
    return d


def sla_model_dict() -> dict[str, Any]:
    d = sla_schema_dict()
    d["doc_uuid"] = d["doc_uuid"].hex
    return d


def sla_schema_dict() -> dict[str, Any]:
    start_date, end_date = random_start_end_dates()
    return {"doc_uuid": uuid4(), "start_date": start_date, "end_date": end_date}


def user_group_model_dict() -> dict[str, str]:
    return user_group_schema_dict()


def user_group_schema_dict() -> dict[str, str]:
    return {"name": random_lower_string()}
