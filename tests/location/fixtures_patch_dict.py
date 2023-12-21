"""Location specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, parametrize

from app.location.models import Location
from app.location.schemas import LocationUpdate
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


def location_patch_not_equal_data(
    *, db_item: Location, new_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Return a dict with new different data.

    The dict has the same keys as the input dict. If the values in the received dict
    differs from the ones in the DB instance, they are kept, otherwise they are
    substituted.

    Args:
    ----
        db_item (Provider): DB instance.
        new_data (dict): Dict with the initial data.
    """
    valid_data = {}
    for k, v in new_data.items():
        valid_data[k] = v
        while db_item.__getattribute__(k) == valid_data[k]:
            schema_type = LocationUpdate.__fields__.get(k).type_
            print(schema_type)
            assert 0
    return valid_data
