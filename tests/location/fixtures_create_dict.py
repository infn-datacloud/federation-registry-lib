"""Location specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import random_lower_string
from tests.location.utils import random_location_all_attr, random_location_required_attr

invalid_create_key_values = [
    ("description", None),
    ("site", None),
    ("country", None),
    ("country", random_lower_string()),
    ("latitude", -181),
    ("latitude", 181),
    ("longitude", -91),
    ("longitude", 91),
]


@fixture
def location_create_minimum_data() -> Dict[str, Any]:
    """Dict with Location mandatory attributes."""
    return random_location_required_attr()


@fixture
def location_create_all_data() -> Dict[str, Any]:
    """Dict with all Location attributes."""
    return random_location_all_attr()


@fixture
@parametrize("k, v", invalid_create_key_values)
def location_create_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_location_required_attr(), k: v}


location_create_valid_data = fixture_union(
    "location_create_valid_data",
    (location_create_minimum_data, location_create_all_data),
    idstyle="explicit",
)
