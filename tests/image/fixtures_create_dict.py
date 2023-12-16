"""Image specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.utils.image import random_os_type
from tests.utils.utils import random_bool, random_lower_string

is_public = {True, False}
invalid_create_key_values = {
    ("description", None),
    ("uuid", None),
    ("name", None),
    ("is_public", None),
    ("cuda_support", None),
    ("gpu_driver", None),
    ("tags", None),
}


@fixture
def image_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Image mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture
def image_create_all_data(
    image_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Image attributes."""
    return {
        **image_create_mandatory_data,
        "is_public": random_bool(),
        "description": random_lower_string(),
        "os_type": random_os_type(),
        "os_distro": random_lower_string(),
        "os_version": random_lower_string(),
        "architecture": random_lower_string(),
        "kernel_id": random_lower_string(),
        "cuda_support": random_bool(),
        "gpu_driver": random_bool(),
        "tags": [random_lower_string()],
    }


@fixture
@parametrize("is_public", is_public)
def image_create_data_with_rel(
    image_create_all_data: Dict[str, Any], is_public: bool
) -> Dict[str, Any]:
    """Dict with relationships attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **image_create_all_data,
        "is_public": is_public,
        "projects": [] if is_public else [uuid4()],
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def image_create_invalid_pair(
    image_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**image_create_mandatory_data, k: v}


@fixture
@parametrize("is_public", is_public)
def image_create_invalid_projects_list_size(
    image_create_mandatory_data: Dict[str, Any], is_public: bool
) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If image is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    return {
        **image_create_mandatory_data,
        "is_public": is_public,
        "projects": [] if not is_public else [uuid4()],
    }


@fixture
def image_create_duplicate_projects(
    image_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    project_uuid = uuid4()
    return {
        **image_create_mandatory_data,
        "is_public": False,
        "projects": [project_uuid, project_uuid],
    }


image_create_valid_data = fixture_union(
    "image_create_valid_data",
    (image_create_mandatory_data, image_create_data_with_rel),
    idstyle="explicit",
)


image_create_invalid_data = fixture_union(
    "image_create_invalid_data",
    (
        image_create_invalid_pair,
        image_create_invalid_projects_list_size,
        image_create_duplicate_projects,
    ),
    idstyle="explicit",
)
