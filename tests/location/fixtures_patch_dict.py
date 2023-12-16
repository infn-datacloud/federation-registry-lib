"""Location specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from tests.common.utils import random_lower_string
from tests.location.utils import random_country, random_latitude, random_longitude

patch_key_values = [
    ("description", random_lower_string()),
    ("site", random_lower_string()),
    ("country", random_country()),
    ("latitude", random_latitude()),
    ("longitude", random_longitude()),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None),
    ("country", random_lower_string()),
    ("latitude", -181),
    ("latitude", 181),
    ("longitude", -91),
    ("longitude", 91),
]


@fixture
@parametrize("k, v", patch_key_values)
def location_patch_valid_data(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Location patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def location_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Location patch schema."""
    return {k: v}
