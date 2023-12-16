"""ComputeService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    ComputeQuotaCreateExtended,
    FlavorCreateExtended,
    ImageCreateExtended,
)
from app.service.enum import ServiceType
from tests.common.utils import random_lower_string, random_url
from tests.services.utils import random_compute_service_name

invalid_create_key_values = [
    ("description", None),
    ("type", None),
    ("type", ServiceType.BLOCK_STORAGE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
    ("endpoint", None),
    ("name", None),
]
relationships_attr = ["flavors", "images", "quotas"]


@fixture
def compute_service_create_mandatory_data() -> Dict[str, Any]:
    """Dict with ComputeService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_compute_service_name()}


@fixture
def compute_service_create_all_data(
    compute_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all ComputeService attributes."""
    return {
        **compute_service_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
@parametrize(attr=relationships_attr)
def compute_service_create_data_passing_empty_list(
    attr: str, compute_service_create_all_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with all Region attributes.

    Passing an empty list is not a problem.
    """
    return {**compute_service_create_all_data, attr: []}


@fixture
def compute_service_create_data_with_flavors(
    compute_service_create_all_data: Dict[str, Any],
    flavor_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    flavor = FlavorCreateExtended(**flavor_create_data_with_rel)
    return {**compute_service_create_all_data, "flavors": [flavor]}


@fixture
def compute_service_create_data_with_images(
    compute_service_create_all_data: Dict[str, Any],
    image_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    image = ImageCreateExtended(**image_create_data_with_rel)
    return {**compute_service_create_all_data, "images": [image]}


@fixture
def compute_service_create_data_with_quotas(
    compute_service_create_all_data: Dict[str, Any],
    compute_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = ComputeQuotaCreateExtended(**compute_quota_create_data_with_rel)
    return {**compute_service_create_all_data, "quotas": [quota]}


@fixture
def compute_service_create_data_with_2_quotas_same_proj(
    compute_service_create_all_data: Dict[str, Any],
    compute_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with 2 quotas on same project.

    A quota has the flag 'per_user' equals to True and the other equal to False.
    """
    quota1 = ComputeQuotaCreateExtended(**compute_quota_create_data_with_rel)
    compute_quota_create_data_with_rel[
        "per_user"
    ] = not compute_quota_create_data_with_rel["per_user"]
    quota2 = ComputeQuotaCreateExtended(**compute_quota_create_data_with_rel)
    return {**compute_service_create_all_data, "quotas": [quota1, quota2]}


@fixture
@parametrize("k, v", invalid_create_key_values)
def compute_service_create_invalid_pair(
    compute_service_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**compute_service_create_mandatory_data}
    data[k] = v
    return data


@fixture
def compute_service_invalid_num_quotas_same_project(
    compute_service_create_mandatory_data: Dict[str, Any],
    compute_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = ComputeQuotaCreateExtended(**compute_quota_create_data_with_rel)
    return {**compute_service_create_mandatory_data, "quotas": [quota, quota]}


@fixture
def compute_service_create_duplicate_flavors(
    compute_service_create_mandatory_data: Dict[str, Any],
    flavor_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the flavor list has duplicate values."""
    flavor = FlavorCreateExtended(**flavor_create_mandatory_data)
    return {**compute_service_create_mandatory_data, "flavors": [flavor, flavor]}


@fixture
def compute_service_create_duplicate_images(
    compute_service_create_mandatory_data: Dict[str, Any],
    image_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the image list has duplicate values."""
    image = ImageCreateExtended(**image_create_mandatory_data)
    return {**compute_service_create_mandatory_data, "images": [image, image]}


compute_service_create_valid_data = fixture_union(
    "compute_service_create_valid_data",
    (
        compute_service_create_mandatory_data,
        compute_service_create_data_with_flavors,
        compute_service_create_data_with_images,
        compute_service_create_data_with_quotas,
        compute_service_create_data_with_2_quotas_same_proj,
    ),
    idstyle="explicit",
)


compute_service_create_invalid_data = fixture_union(
    "compute_service_create_invalid_data",
    (
        compute_service_create_invalid_pair,
        compute_service_invalid_num_quotas_same_project,
        compute_service_create_duplicate_flavors,
        compute_service_create_duplicate_images,
    ),
    idstyle="explicit",
)
