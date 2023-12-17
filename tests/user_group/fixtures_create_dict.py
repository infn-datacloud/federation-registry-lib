"""UserGroup specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.user_group.utils import (
    random_user_group_all_attr,
    random_user_group_required_attr,
)

invalid_create_key_values = [("description", None), ("name", None)]


@fixture
def user_group_create_minimum_data() -> Dict[str, Any]:
    """Dict with UserGroup mandatory attributes."""
    return random_user_group_required_attr()


@fixture
def user_group_create_data_with_rel(
    sla_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**random_user_group_all_attr(), "sla": sla_create_data_with_rel}


@fixture
@parametrize("k, v", invalid_create_key_values)
def user_group_create_invalid_pair(
    user_group_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**user_group_create_data_with_rel, k: v}


user_group_create_valid_data = fixture_union(
    "user_group_create_valid_data",
    (user_group_create_data_with_rel,),
    idstyle="explicit",
)


user_group_create_invalid_data = fixture_union(
    "user_group_create_invalid_data",
    (user_group_create_minimum_data, user_group_create_invalid_pair),
    idstyle="explicit",
)
