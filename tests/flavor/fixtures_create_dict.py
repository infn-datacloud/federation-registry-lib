"""Flavor specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)

is_public = [True, False]
gpu_details = [
    ("gpu_model", random_lower_string()),  # gpus is 0
    ("gpu_vendor", random_lower_string()),  # gpus is 0
]
invalid_create_key_values = [
    ("description", None),
    ("uuid", None),
    ("name", None),
    ("is_public", None),
    ("disk", -1),
    ("ram", -1),
    ("vcpus", -1),
    ("swap", -1),
    ("ephemeral", -1),
    *gpu_details,
]


@fixture
def flavor_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Flavor mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture
def flavor_create_all_data(
    flavor_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Flavor attributes."""
    return {
        **flavor_create_mandatory_data,
        "is_public": True,
        "description": random_lower_string(),
        "disk": random_non_negative_int(),
        "ram": random_non_negative_int(),
        "vcpus": random_non_negative_int(),
        "swap": random_non_negative_int(),
        "ephemeral": random_non_negative_int(),
        "infiniband": random_bool(),
        "gpus": random_positive_int(),
        "gpu_model": random_lower_string(),
        "gpu_vendor": random_lower_string(),
        "local_storage": random_lower_string(),
    }


@fixture
@parametrize(is_public=is_public)
def flavor_create_data_with_rel(
    is_public: bool, flavor_create_all_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with relationships attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **flavor_create_all_data,
        "is_public": is_public,
        "projects": [] if is_public else [uuid4()],
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def flavor_create_invalid_pair(
    flavor_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**flavor_create_mandatory_data, k: v}


@fixture
@parametrize(is_public=is_public)
def flavor_create_invalid_projects_list_size(
    flavor_create_mandatory_data: Dict[str, Any], is_public: bool
) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If flavor is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    return {
        **flavor_create_mandatory_data,
        "is_public": is_public,
        "projects": None if not is_public else [uuid4()],
    }


@fixture
def flavor_create_duplicate_projects(flavor_create_mandatory_data: Dict[str, Any]):
    """Invalid case: the project list has duplicate values."""
    project_uuid = uuid4()
    return {
        **flavor_create_mandatory_data,
        "is_public": is_public,
        "projects": [project_uuid, project_uuid],
    }


flavor_create_valid_data = fixture_union(
    "flavor_create_valid_data",
    (flavor_create_mandatory_data, flavor_create_data_with_rel),
    idstyle="explicit",
)

flavor_create_invalid_data = fixture_union(
    "flavor_create_invalid_data",
    (
        flavor_create_invalid_pair,
        flavor_create_invalid_projects_list_size,
        flavor_create_duplicate_projects,
    ),
    idstyle="explicit",
)
