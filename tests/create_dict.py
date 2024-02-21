from typing import Any, Dict
from uuid import uuid4

from tests.utils import random_date, random_lower_string


def auth_method_dict() -> Dict[str, str]:
    return {"idp_name": random_lower_string(), "protocol": random_lower_string()}


def flavor_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def identity_provider_dict() -> Dict[str, str]:
    return {"endpoint": random_lower_string(), "group_claim": random_lower_string()}


def image_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def location_dict() -> Dict[str, str]:
    return {"site": random_lower_string(), "country": random_lower_string()}


def network_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def project_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def provider_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "type": random_lower_string()}


def quota_dict():
    return {"type": random_lower_string()}


def region_dict() -> Dict[str, str]:
    return {"name": random_lower_string()}


def service_dict() -> Dict[str, str]:
    return {
        "type": random_lower_string(),
        "endpoint": random_lower_string(),
        "name": random_lower_string(),
    }


def sla_dict() -> Dict[str, Any]:
    return {
        "doc_uuid": uuid4().hex,
        "start_date": random_date(),
        "end_date": random_date(),
    }


def user_group_dict() -> Dict[str, str]:
    return {"name": random_lower_string()}
