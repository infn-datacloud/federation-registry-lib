from typing import Generator

from ..utils.service import create_random_service
from ..utils.utils import random_lower_string, random_url
from ...service.crud import service
from ...service.schemas import ServiceCreate, ServiceUpdate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    endpoint = random_url()
    item_in = ServiceCreate(endpoint=endpoint, description=description)
    item = service.create(obj_in=item_in)
    assert item.description == description
    assert item.endpoint == endpoint


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    endpoint = random_url()
    item_in = ServiceCreate(endpoint=endpoint)
    item = service.create(obj_in=item_in)
    assert item.description == ""
    assert item.endpoint == endpoint


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_service()
    stored_item = service.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.endpoint == stored_item.endpoint

    stored_item = service.get(endpoint=item.endpoint)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.endpoint == stored_item.endpoint


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_service()
    description2 = random_lower_string()
    endpoint2 = random_url()
    item_update = ServiceUpdate(endpoint=endpoint2, description=description2)
    item2 = service.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == description2
    assert item2.endpoint == endpoint2


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
