from typing import Generator

from ..utils.service_type import create_random_service_type, random_name
from ..utils.utils import random_lower_string
from ...service_type.crud import service_type
from ...service_type.schemas import ServiceTypeCreate, ServiceTypeUpdate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    name = random_name()
    item_in = ServiceTypeCreate(name=name, description=description)
    item = service_type.create(obj_in=item_in)
    assert item.description == description
    assert item.name == name


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_name()
    item_in = ServiceTypeCreate(name=name)
    item = service_type.create(obj_in=item_in)
    assert item.description == ""
    assert item.name == name


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_service_type()
    stored_item = service_type.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.name == stored_item.name

    stored_item = service_type.get(name=item.name)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.name == stored_item.name


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_service_type()
    item2 = create_random_service_type()
    stored_items = service_type.get_multi()
    assert len(stored_items) == 2

    stored_items = service_type.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = service_type.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].name == item.name

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = service_type.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = service_type.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_service_type()
    description2 = random_lower_string()
    name2 = random_name()
    item_update = ServiceTypeUpdate(name=name2, description=description2)
    item2 = service_type.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == description2
    assert item2.name == name2


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_service_type()
    item2 = service_type.remove(db_obj=item)
    item3 = service_type.get(uid=item.uid)
    assert item2 is True
    assert item3 is None


# TODO
# Presence of UniqueIdProperty creates a new instance
# with same name but different UUID. The following test fails
#
# def test_create_item_duplicate_name(setup_and_teardown_db) -> None:
#    name = random_lower_string()
#    description = random_lower_string()
#    item_in = ServiceTypeCreate(name=name, description=description)
#    item = service_type.create(obj_in=item_in)
#    assert item.name == name
#    assert item.description == description
#
#    item_in = ServiceTypeCreate(name=name)
#    item2 = service_type.create(obj_in=item_in)
#    assert item2.uid == item.uid
#    assert item2.name == item.name
#    assert item2.description == item.description
