from random import choice, randrange
from typing import Union

from app.location.models import Location
from app.location.schemas import (
    LocationCreate,
    LocationRead,
    LocationReadShort,
    LocationUpdate,
)
from app.location.schemas_extended import LocationReadExtended
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


def create_random_location_patch(default: bool = False) -> LocationUpdate:
    if default:
        return LocationUpdate()
    description = random_lower_string()
    site = random_lower_string()
    country = random_country()
    latitude = random_latitude()
    longitude = random_longitude()
    return LocationUpdate(
        description=description,
        site=site,
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


def validate_create_location_attrs(
    *, obj_in: LocationCreate, db_item: Location
) -> None:
    validate_location_attrs(obj_in=obj_in, db_item=db_item)


def validate_read_location_attrs(
    *,
    obj_out: Union[LocationRead, LocationReadShort, LocationReadExtended],
    db_item: Location
) -> None:
    assert db_item.uid == obj_out.uid
    validate_location_attrs(obj_in=obj_out, db_item=db_item)

    if isinstance(obj_out, LocationReadExtended):
        assert len(db_item.regions) == len(obj_out.regions)
        for db_reg, reg_out in zip(db_item.regions, obj_out.regions):
            assert db_reg.uid == reg_out.uid
