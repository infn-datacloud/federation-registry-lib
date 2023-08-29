from typing import Generator

from app.location.crud import location
from app.location.schemas import LocationCreate
from app.tests.utils.location import (
    create_random_location,
    create_random_update_location_data,
    random_country,
    random_latitude,
    random_longitude,
)
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import random_lower_string


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


def test_create_item_with_provider(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    country = random_country()
    item_in = LocationCreate(name=name, country=country)
    provider = create_random_provider()
    item = location.create(obj_in=item_in, provider=provider)
    assert item.description == ""
    assert item.name == name
    assert item.country == country
    assert item.latitude is None
    assert item.longitude is None
    item_providers = item.providers.all()
    assert len(item_providers) == 1
    assert item_providers[0].uid == provider.uid


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


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_location()
    item2 = create_random_location()
    stored_items = location.get_multi()
    assert len(stored_items) == 2

    stored_items = location.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = location.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].name == item.name
    assert stored_items[0].country == item.country
    assert stored_items[0].latitude == item.latitude
    assert stored_items[0].longitude == item.longitude

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = location.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = location.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_location()
    item_update = create_random_update_location_data()
    item2 = location.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.name == item_update.name
    assert item2.country == item_update.country
    assert item2.latitude == item_update.latitude
    assert item2.longitude == item_update.longitude

    item_update = create_random_update_location_data()
    item2 = location.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.name == item_update.name
    assert item2.country == item_update.country
    assert item2.latitude == item_update.latitude
    assert item2.longitude == item_update.longitude


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_location()
    item2 = location.remove(db_obj=item)
    item3 = location.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
