"""Project specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.project.utils import random_project_all_attr, random_project_required_attr

invalid_create_key_values = [("description", None), ("uuid", None), ("name", None)]


@fixture
def project_create_minimum_data() -> Dict[str, Any]:
    """Dict with Project mandatory attributes."""
    return random_project_required_attr()


@fixture
def project_create_all_data() -> Dict[str, Any]:
    """Dict with all Project attributes."""
    return random_project_all_attr()


@fixture
@parametrize("k, v", invalid_create_key_values)
def project_create_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_project_required_attr(), k: v}


project_create_valid_data = fixture_union(
    "project_create_valid_data",
    (project_create_minimum_data, project_create_all_data),
    idstyle="explicit",
)
