from typing import Any, Dict
from uuid import uuid4

from tests.utils import random_country, random_date, random_lower_string, random_url


def auth_method_dict() -> Dict[str, str]:
    return {"idp_name": random_lower_string(), "protocol": random_lower_string()}


def flavor_model_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def flavor_schema_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def identity_provider_model_dict() -> Dict[str, str]:
    return {"endpoint": random_lower_string(), "group_claim": random_lower_string()}


def identity_provider_schema_dict() -> Dict[str, str]:
    return {"endpoint": random_url(), "group_claim": random_lower_string()}


def image_model_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def image_schema_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def location_model_dict() -> Dict[str, str]:
    return {"site": random_lower_string(), "country": random_lower_string()}


def location_schema_dict() -> Dict[str, str]:
    return {"site": random_lower_string(), "country": random_country()}


def network_model_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def network_schema_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4()}


def project_model_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "uuid": uuid4().hex}


def provider_model_dict() -> Dict[str, str]:
    return {"name": random_lower_string(), "type": random_lower_string()}


def quota_model_dict():
    return {"type": random_lower_string()}


def region_model_dict() -> Dict[str, str]:
    return {"name": random_lower_string()}


def service_model_dict() -> Dict[str, str]:
    return {
        "type": random_lower_string(),
        "endpoint": random_lower_string(),
        "name": random_lower_string(),
    }


def sla_model_dict() -> Dict[str, Any]:
    return {
        "doc_uuid": uuid4().hex,
        "start_date": random_date(),
        "end_date": random_date(),
    }


def user_group_model_dict() -> Dict[str, str]:
    return {"name": random_lower_string()}
