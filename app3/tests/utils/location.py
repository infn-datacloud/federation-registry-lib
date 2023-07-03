from random import choice, randrange
from pycountry import countries

from .utils import random_lower_string
from ...location.crud import location
from ...location.models import Location
from ...location.schemas import LocationCreate, LocationUpdate


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


def create_random_update_location_data() -> LocationUpdate:
    description = random_lower_string()
    name = random_lower_string()
    country = random_country()
    latitude = random_latitude()
    longitude = random_longitude()
    return LocationUpdate(
        description=description,
        name=name,
        country=country,
        latitude=latitude,
        longitude=longitude,
    )


def random_country() -> str:
    return choice([i.name for i in countries])


def random_latitude() -> float:
    return float(randrange(-180, 180))


def random_longitude() -> float:
    return float(randrange(-90, 90))
