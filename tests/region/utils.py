"""Region utilities."""
from typing import Any, Dict

from tests.common.utils import random_lower_string


def random_region_required_attr() -> Dict[str, Any]:
    """Return a dict with the Region required attributes initialized."""
    return {"name": random_lower_string()}


def random_region_all_attr() -> Dict[str, Any]:
    """Dict with Region mandatory attributes."""
    return {**random_region_required_attr(), "description": random_lower_string()}
