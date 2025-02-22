from random import choice, randint, random
from typing import Any
from uuid import uuid4

from pycountry import countries

from fedreg.image.enum import ImageOS
from fedreg.models import BaseNodeRead
from fedreg.provider.enum import ProviderStatus, ProviderType
from fedreg.service.enum import (
    BlockStorageServiceName,
    ComputeServiceName,
    IdentityServiceName,
    NetworkServiceName,
    ObjectStoreServiceName,
    ServiceType,
)
from tests.utils import (
    random_lower_string,
    random_non_negative_int,
    random_start_end_dates,
    random_url,
)


def auth_method_schema_dict() -> dict[str, Any]:
    return {"idp_name": random_lower_string(), "protocol": random_lower_string()}


def flavor_schema_dict() -> dict[str, Any]:
    """Return a dict with the flavor pydantic mandatory attributes.

    If 'read' is true add the 'uid' attribute.
    """
    return {"name": random_lower_string(), "uuid": uuid4()}


def identity_provider_schema_dict() -> dict[str, Any]:
    return {"endpoint": random_url(), "group_claim": random_lower_string()}


def image_schema_dict() -> dict[str, Any]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def location_schema_dict() -> dict[str, Any]:
    return {"site": random_lower_string(), "country": random_country()}


def network_schema_dict() -> dict[str, Any]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def project_schema_dict() -> dict[str, Any]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def provider_schema_dict() -> dict[str, Any]:
    return {"name": random_lower_string(), "type": random_provider_type()}


def quota_schema_dict() -> dict[str, Any]:
    return {}


def region_schema_dict() -> dict[str, Any]:
    return {"name": random_lower_string()}


def service_schema_dict(srv_type: ServiceType | None = None) -> dict[str, Any]:
    d = {"endpoint": random_url()}
    if srv_type is not None:
        d["name"] = random_service_name(srv_type)
    return d


def sla_schema_dict() -> dict[str, Any]:
    start_date, end_date = random_start_end_dates()
    return {"doc_uuid": uuid4(), "start_date": start_date, "end_date": end_date}


def user_group_schema_dict() -> dict[str, Any]:
    return {"name": random_lower_string()}


def quota_valid_dict(data: dict[str, Any], *args, **kwargs) -> dict[str, Any]:
    for k in args:
        if k in ("description",):
            data[k] = random_lower_string()
        elif k in ("per_user", "usage"):
            data[k] = True
        elif k in (
            "gigabytes",
            "volumes",
            "per_volume_gigabytes",
            "cores",
            "instances",
            "ram",
            "public_ips",
            "networks",
            "ports",
            "security_groups",
            "security_group_rules",
            "bytes",
            "containers",
            "objects",
        ):
            data[k] = random_non_negative_int()
        else:
            raise AttributeError(f"attribute {k} not found in class definition")
    return data


def quota_invalid_dict(data: dict[str, Any], *args, **kwargs) -> dict[str, Any]:
    return data


def random_country() -> str:
    """Return random country."""
    return choice([i.name for i in countries])


def random_latitude() -> float:
    """Return a valid latitude value."""
    return randint(-90, 89) + random()


def random_longitude() -> float:
    """Return a valid longitude value."""
    return randint(-180, 179) + random()


def random_provider_type() -> ProviderType:
    return choice([i for i in ProviderType])


def random_provider_status() -> ProviderStatus:
    return choice([i for i in ProviderStatus])


def random_service_name(
    srv_type: ServiceType,
) -> (
    BlockStorageServiceName
    | ComputeServiceName
    | IdentityServiceName
    | NetworkServiceName
    | ObjectStoreServiceName
):
    if srv_type == ServiceType.BLOCK_STORAGE:
        enum_cls = BlockStorageServiceName
    if srv_type == ServiceType.COMPUTE:
        enum_cls = ComputeServiceName
    if srv_type == ServiceType.IDENTITY:
        enum_cls = IdentityServiceName
    if srv_type == ServiceType.NETWORK:
        enum_cls = NetworkServiceName
    if srv_type == ServiceType.OBJECT_STORE:
        enum_cls = ObjectStoreServiceName
    return choice([i for i in enum_cls])


def random_image_os_type() -> ImageOS:
    return choice([i for i in ImageOS])


def detect_public_extended_details(read_class: type[BaseNodeRead]) -> tuple[bool, bool]:
    """From class name detect if it public or not, extended or not."""
    cls_name = read_class.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return is_public, is_extended
