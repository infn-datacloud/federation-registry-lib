"""Location specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import random_lower_string
from tests.location.utils import random_country, random_latitude, random_longitude

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
def location_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Location mandatory attributes."""
    return {"site": random_lower_string(), "country": random_country()}


@fixture
def location_create_all_data(
    location_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Location attributes."""
    return {
        **location_create_mandatory_data,
        "description": random_lower_string(),
        "latitude": random_latitude(),
        "longitude": random_longitude(),
    }


@fixture
@parametrize("k, v", invalid_create_key_values)
def location_create_invalid_pair(
    location_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**location_create_mandatory_data}
    data[k] = v
    return data


location_create_valid_data = fixture_union(
    "location_create_valid_data",
    (location_create_mandatory_data, location_create_all_data),
    idstyle="explicit",
)


location_create_invalid_data = fixture_union(
    "location_create_invalid_data", (location_create_invalid_pair,), idstyle="explicit"
)
