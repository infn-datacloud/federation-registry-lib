from random import choice, randrange

from app.location.models import Location
from app.location.schemas import LocationCreate, LocationUpdate
from app.tests.utils.utils import random_lower_string
from pycountry import countries


def create_random_location(*, default: bool = False) -> LocationCreate:
    site = random_lower_string()
    country = random_country()
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "latitude": random_latitude(),
            "longitude": random_longitude(),
        }
    return LocationCreate(site=site, country=country, **kwargs)


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


def validate_location_attrs(*, obj_in: LocationCreate, db_item: Location) -> None:
    assert db_item.description == obj_in.description
    assert db_item.site == obj_in.site
    assert db_item.country == obj_in.country
    assert db_item.latitude == obj_in.latitude
    assert db_item.longitude == obj_in.longitude
