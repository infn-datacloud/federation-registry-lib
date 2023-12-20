"""Region utilities."""
from typing import Any, Dict

from app.region.schemas import RegionBase
from tests.common.utils import random_bool, random_lower_string


def random_region_required_attr() -> Dict[str, Any]:
    """Return a dict with the Region required attributes initialized."""
    return {"name": random_lower_string()}


def random_region_all_attr() -> Dict[str, Any]:
    """Dict with Region mandatory attributes."""
    return {**random_region_required_attr(), "description": random_lower_string()}


def random_region_all_no_default_attr() -> Dict[str, Any]:
    """Dict with Region no default values."""
    data = random_region_all_attr()
    for k, v in RegionBase.__fields__.items():
        default = v.get_default()
        while data[k] == default:
            if v.type_ == bool:
                data[k] = random_bool()
    return data
