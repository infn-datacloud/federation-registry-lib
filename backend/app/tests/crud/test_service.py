from typing import Generator

from app.service.crud import service
from app.service.schemas import ServiceCreate
from app.tests.utils.provider import create_random_provider
from app.tests.utils.service import (
    create_random_service,
    create_random_update_service_data,
    random_service_type,
)
from app.tests.utils.utils import random_lower_string, random_url


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    endpoint = random_url()
    service_type = random_service_type()
    item_in = ServiceCreate(
        endpoint=endpoint, description=description, type=service_type
    )
    item = service.create(obj_in=item_in, provider=create_random_provider())
    assert item.description == description
    assert item.endpoint == endpoint
    assert item.type == service_type


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    endpoint = random_url()
    service_type = random_service_type()
    item_in = ServiceCreate(endpoint=endpoint, type=service_type)
    item = service.create(obj_in=item_in, provider=create_random_provider())
    assert item.description == ""
    assert item.endpoint == endpoint
    assert item.type == service_type


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_service()
    stored_item = service.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.endpoint == stored_item.endpoint
    assert item.type == stored_item.type

    stored_item = service.get(endpoint=item.endpoint)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.endpoint == stored_item.endpoint
    assert item.type == stored_item.type


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_service()
    item2 = create_random_service()
    stored_items = service.get_multi()
    assert len(stored_items) == 2

    stored_items = service.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = service.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].endpoint == item.endpoint

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = service.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = service.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_service()
    item_update = create_random_update_service_data()
    item2 = service.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.endpoint == item_update.endpoint

    item_update = create_random_update_service_data()
    item2 = service.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.endpoint == item_update.endpoint


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_service()
    item2 = service.remove(db_obj=item)
    item3 = service.get(uid=item.uid)
    assert item2 is True
    assert item3 is None


# TODO
# Presence of UniqueIdProperty creates a new instance
# with same endpoint but different UUID. The following test fails
#
# def test_create_item_duplicate_endpoint(setup_and_teardown_db) -> None:
#    endpoint = random_lower_string()
#    description = random_lower_string()
#    item_in = ServiceCreate(endpoint=endpoint, description=description)
#    item = service.create(obj_in=item_in)
#    assert item.endpoint == endpoint
#    assert item.description == description
#
#    item_in = ServiceCreate(endpoint=endpoint)
#    item2 = service.create(obj_in=item_in)
#    assert item2.uid == item.uid
#    assert item2.endpoint == item.endpoint
#    assert item2.description == item.description
