"""Provider specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import (
    random_bool,
    random_email,
    random_lower_string,
)
from tests.provider.utils import random_status, random_type

patch_key_values = [
    ("description", random_lower_string()),
    ("name", random_lower_string()),
    ("type", random_type()),
    ("status", random_status()),
    ("is_public", random_bool()),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None),
    ("type", random_lower_string()),
    ("status", None),
    ("status", random_lower_string()),
    ("is_public", None),
]


@fixture
@parametrize("k, v", patch_key_values)
def provider_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Provider patch schema."""
    return {k: v}


@fixture
def provider_patch_valid_data_for_support_emails() -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema. Tags details."""
    return {"support_emails": [random_email()]}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def provider_patch_invalid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Provider patch schema."""
    return {k: v}


@fixture
@parametrize(support_emails={None, random_lower_string()})
def provider_patch_invalid_data_for_support_emails(support_emails) -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema. Tags details."""
    support_emails = [support_emails] if support_emails else support_emails
    return {"support_emails": support_emails}


provider_patch_valid_data = fixture_union(
    "provider_patch_valid_data",
    (
        provider_patch_valid_data_single_attr,
        provider_patch_valid_data_for_support_emails,
    ),
    idstyle="explicit",
)


provider_patch_invalid_data = fixture_union(
    "provider_patch_invalid_data",
    (
        provider_patch_invalid_data_single_attr,
        provider_patch_invalid_data_for_support_emails,
    ),
    idstyle="explicit",
)
