from typing import Generator

from ..utils.location import (
    create_random_location,
    random_country,
    random_latitude,
    random_longitude,
)
from ..utils.utils import random_lower_string
from ...location.crud import location
from ...location.schemas import LocationCreate, LocationUpdate


def test_create_item(setup_and_teardown_db: Generator) -> None:
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
    item = location.create(obj_in=item_in)
    assert item.description == description
    assert item.name == name
    assert item.country == country
    assert item.latitude == latitude
    assert item.longitude == longitude


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    country = random_country()
    item_in = LocationCreate(name=name, country=country)
    item = location.create(obj_in=item_in)
    assert item.description == ""
    assert item.name == name
    assert item.country == country
    assert item.latitude is None
    assert item.longitude is None


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_location()
    stored_item = location.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.name == stored_item.name
    assert item.country == stored_item.country
    assert item.latitude == stored_item.latitude
    assert item.longitude == stored_item.longitude


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_location()
    description2 = random_lower_string()
    name2 = random_lower_string()
    country2 = random_country()
    latitude2 = random_latitude()
    longitude2 = random_longitude()
    item_update = LocationUpdate(
        description=description2,
        name=name2,
        country=country2,
        latitude=latitude2,
        longitude=longitude2,
    )
    item2 = location.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == description2
    assert item2.name == name2
    assert item2.country == country2
    assert item2.latitude == latitude2
    assert item2.longitude == longitude2


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_location()
    item2 = location.remove(db_obj=item)
    item3 = location.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
