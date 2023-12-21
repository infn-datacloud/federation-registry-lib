"""IdentityProvider specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.identity_provider.utils import (
    random_identity_provider_all_attr,
    random_identity_provider_required_attr,
    random_identity_provider_required_rel,
)
from tests.user_group.utils import (
    random_user_group_required_rel,
)

invalid_create_key_values = [
    ("description", None),
    ("endpoint", None),
    ("group_claim", None),
]


@fixture
def identity_provider_create_minimum_data() -> Dict[str, Any]:
    """Dict with IdentityProvider mandatory attributes."""
    return random_identity_provider_required_attr()


@fixture
def identity_provider_create_data_with_rel() -> Dict[str, Any]:
    """Dict with IdentityProvider mandatory attributes."""
    return {
        **random_identity_provider_all_attr(),
        **random_identity_provider_required_rel(),
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def identity_provider_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {
        **random_identity_provider_required_attr(),
        **random_identity_provider_required_rel(),
        k: v,
    }


@fixture
def identity_provider_create_invalid_user_group_list_size() -> Dict[str, Any]:
    """User group list can't be empty."""
    return {
        **random_identity_provider_required_attr(),
        **random_identity_provider_required_rel(),
        "user_groups": [],
    }


@fixture
def identity_provider_create_duplicate_user_groups() -> Dict[str, Any]:
    """Invalid case: the user group list has duplicate values."""
    relationships = random_identity_provider_required_rel()
    user_group = relationships["user_groups"][0]
    relationships["user_groups"].append(
        {**user_group, **random_user_group_required_rel()}
    )
    return {**random_identity_provider_required_attr(), **relationships}


identity_provider_create_valid_data = fixture_union(
    "identity_provider_create_valid_data",
    (identity_provider_create_data_with_rel,),
    idstyle="explicit",
)


identity_provider_create_invalid_data = fixture_union(
    "identity_provider_create_invalid_data",
    (
        identity_provider_create_minimum_data,
        identity_provider_create_invalid_pair,
        identity_provider_create_invalid_user_group_list_size,
        identity_provider_create_duplicate_user_groups,
    ),
    idstyle="explicit",
)
