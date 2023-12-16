"""UserGroup specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import random_lower_string

invalid_create_key_values = [("description", None), ("name", None)]


@fixture
def user_group_create_mandatory_data() -> Dict[str, Any]:
    """Dict with UserGroup mandatory attributes."""
    return {"name": random_lower_string()}


@fixture
def user_group_create_all_data(
    user_group_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all UserGroup attributes."""
    return {**user_group_create_mandatory_data, "description": random_lower_string()}


@fixture
def user_group_create_data_with_rel(
    user_group_create_all_data: Dict[str, Any], sla_create_data_with_rel: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**user_group_create_all_data, "sla": sla_create_data_with_rel}


@fixture
@parametrize("k, v", invalid_create_key_values)
def user_group_create_invalid_pair(
    user_group_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**user_group_create_mandatory_data, k: v}


user_group_create_valid_data = fixture_union(
    "user_group_create_valid_data",
    (user_group_create_data_with_rel,),
    idstyle="explicit",
)


user_group_create_invalid_data = fixture_union(
    "user_group_create_invalid_data",
    (user_group_create_mandatory_data, user_group_create_invalid_pair),
    idstyle="explicit",
)
