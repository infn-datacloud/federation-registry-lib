from random import choice, randrange
from pycountry import countries

from .utils import random_lower_string
from ...location.crud import location
from ...location.models import Location
from ...location.schemas import LocationCreate


def create_random_location() -> Location:
    description = random_lower_string()
    name = random_lower_string()
    country = random_country()
    latitude = random_latitude()
    longitude = random_longitude()
    item_in = LocationCreate(
        description=description,
        name=name,
        country=country,
        latitude=latitude,
        longitude=longitude,
    )
    return location.create(obj_in=item_in)


def random_country() -> str:
    return choice([i.name for i in countries])


def random_latitude() -> float:
    return float(randrange(-180, 180))


def random_longitude() -> float:
    return float(randrange(-90, 90))
