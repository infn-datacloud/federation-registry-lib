"""Image specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.image.utils import (
    IS_PUBLIC,
    random_image_all_attr,
    random_image_required_attr,
    random_image_required_rel,
)

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
def image_create_minimum_data() -> Dict[str, Any]:
    """Dict with Image mandatory attributes."""
    return random_image_required_attr()


@fixture
@parametrize(is_public=IS_PUBLIC)
def image_create_data_with_rel(is_public: bool) -> Dict[str, Any]:
    """Dict with relationships attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **random_image_all_attr(),
        **random_image_required_rel(is_public),
        "is_public": is_public,
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def image_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_image_required_attr(), k: v}


@fixture
@parametrize(is_public=IS_PUBLIC)
def image_create_invalid_projects_list_size(is_public: bool) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If image is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    return {
        **random_image_required_attr(),
        "is_public": is_public,
        "projects": [] if not is_public else [uuid4()],
    }


@fixture
def image_create_duplicate_projects() -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    project_uuid = uuid4()
    return {
        **random_image_required_attr(),
        "is_public": False,
        "projects": [project_uuid, project_uuid],
    }


image_create_valid_data = fixture_union(
    "image_create_valid_data",
    (image_create_minimum_data, image_create_data_with_rel),
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
