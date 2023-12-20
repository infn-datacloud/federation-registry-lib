"""Region specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from tests.common.utils import random_lower_string

patch_key_values = [
    ("description", random_lower_string()),
    ("name", random_lower_string()),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None)
]


@fixture
@parametrize("k, v", patch_key_values)
def region_patch_valid_data(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Region patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def region_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Region patch schema."""
    return {k: v}
