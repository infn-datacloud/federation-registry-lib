"""Flavor specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.flavor.utils import (
    GPU_DETAILS,
    IS_PUBLIC,
    random_flavor_all_attr,
    random_flavor_required_attr,
)

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
    *GPU_DETAILS,
]


@fixture
def flavor_create_minimum_data() -> Dict[str, Any]:
    """Dict with Flavor mandatory attributes."""
    return random_flavor_required_attr()


@fixture
@parametrize(is_public=IS_PUBLIC)
def flavor_create_data_with_rel(is_public: bool) -> Dict[str, Any]:
    """Dict with relationships attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **random_flavor_all_attr(),
        "is_public": is_public,
        "projects": [] if is_public else [uuid4()],
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def flavor_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_flavor_required_attr(), k: v}


@fixture
@parametrize(is_public=IS_PUBLIC)
def flavor_create_invalid_projects_list_size(is_public: bool) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If flavor is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    return {
        **random_flavor_required_attr(),
        "is_public": is_public,
        "projects": None if not is_public else [uuid4()],
    }


@fixture
def flavor_create_duplicate_projects() -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    project_uuid = uuid4()
    return {
        **random_flavor_required_attr(),
        "is_public": False,
        "projects": [project_uuid, project_uuid],
    }


flavor_create_valid_data = fixture_union(
    "flavor_create_valid_data",
    (flavor_create_minimum_data, flavor_create_data_with_rel),
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
