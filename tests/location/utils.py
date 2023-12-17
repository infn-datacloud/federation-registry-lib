"""Location utilities."""
from random import choice, randrange
from typing import Any, Dict

from pycountry import countries

from tests.common.utils import random_lower_string


def random_location_required_attr() -> Dict[str, Any]:
    """Return a dict with the Location required attributes initialized."""
    return {"site": random_lower_string(), "country": random_country()}


def random_location_all_attr() -> Dict[str, Any]:
    """Dict with all Location attributes."""
    return {
        **random_location_required_attr(),
        "description": random_lower_string(),
        "latitude": random_latitude(),
        "longitude": random_longitude(),
    }


def random_country() -> str:
    """Return random country."""
    return choice([i.name for i in countries])


def random_latitude() -> float:
    """Return random acceptable value for latitude."""
    return float(randrange(-180, 180))


def random_longitude() -> float:
    """Return random acceptable value for longitude."""
    return float(randrange(-90, 90))
