"""Project specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import random_lower_string

invalid_create_key_values = [("description", None), ("uuid", None), ("name", None)]


@fixture
def project_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Project mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture
def project_create_all_data(
    project_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Project attributes."""
    return {**project_create_mandatory_data, "description": random_lower_string()}


@fixture
@parametrize("k, v", invalid_create_key_values)
def project_create_invalid_pair(
    project_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**project_create_mandatory_data}
    data[k] = v
    return data


project_create_valid_data = fixture_union(
    "project_create_valid_data",
    (project_create_mandatory_data, project_create_all_data),
    idstyle="explicit",
)

project_create_invalid_data = fixture_union(
    "project_create_invalid_data", (project_create_invalid_pair,), idstyle="explicit"
)
