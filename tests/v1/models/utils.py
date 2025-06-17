from typing import Any

from fedreg.v1.service.enum import ServiceType
from tests.v1.schemas.utils import (
    auth_method_schema_dict,
    flavor_schema_dict,
    identity_provider_schema_dict,
    image_schema_dict,
    location_schema_dict,
    network_schema_dict,
    project_schema_dict,
    provider_schema_dict,
    quota_schema_dict,
    region_schema_dict,
    service_schema_dict,
    sla_schema_dict,
    user_group_schema_dict,
)
from tests.v1.utils import random_lower_string


def auth_method_model_dict() -> dict[str, Any]:
    return auth_method_schema_dict()


def flavor_model_dict() -> dict[str, Any]:
    """Return a dict with the flavor neomodel mandatory attributes."""
    d = flavor_schema_dict()
    d["uuid"] = d["uuid"].hex
    return d


def identity_provider_model_dict() -> dict[str, Any]:
    d = identity_provider_schema_dict()
    d["endpoint"] = str(d["endpoint"])
    return d


def image_model_dict() -> dict[str, Any]:
    d = image_schema_dict()
    d["uuid"] = d["uuid"].hex
    return d


def location_model_dict() -> dict[str, Any]:
    return location_schema_dict()


def network_model_dict() -> dict[str, Any]:
    d = network_schema_dict()
    d["uuid"] = d["uuid"].hex
    return d


def project_model_dict() -> dict[str, Any]:
    d = project_schema_dict()
    d["uuid"] = d["uuid"].hex
    return d


def provider_model_dict() -> dict[str, Any]:
    d = provider_schema_dict()
    d["type"] = d["type"].value
    return d


def quota_model_dict() -> dict[str, Any]:
    return quota_schema_dict()


def region_model_dict() -> dict[str, Any]:
    return region_schema_dict()


def service_model_dict(srv_type: ServiceType | None = None) -> dict[str, Any]:
    d = service_schema_dict(srv_type)
    d["endpoint"] = str(d["endpoint"])
    srv_name = d.get("name", None)
    d["name"] = random_lower_string() if srv_name is None else srv_name.value
    if srv_name is None:
        d["type"] = random_lower_string()
    return d


def sla_model_dict() -> dict[str, Any]:
    d = sla_schema_dict()
    d["doc_uuid"] = d["doc_uuid"].hex
    return d


def user_group_model_dict() -> dict[str, Any]:
    return user_group_schema_dict()
