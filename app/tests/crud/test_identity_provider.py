from typing import Generator

from ..utils.identity_provider import (
    create_random_identity_provider,
    create_random_update_identity_provider_data,
)
from ..utils.utils import random_lower_string, random_url
from ...identity_provider.crud import identity_provider
from ...identity_provider.schemas import IdentityProviderCreate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    endpoint = random_url()
    item_in = IdentityProviderCreate(
        description=description, endpoint=endpoint
    )
    item = identity_provider.create(obj_in=item_in)
    assert item.description == description
    assert item.endpoint == endpoint


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    endpoint = random_url()
    item_in = IdentityProviderCreate(endpoint=endpoint)
    item = identity_provider.create(obj_in=item_in)
    assert item.description == ""
    assert item.endpoint == endpoint


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    stored_item = identity_provider.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.endpoint == stored_item.endpoint

    stored_item = identity_provider.get(endpoint=item.endpoint)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.endpoint == stored_item.endpoint


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    item2 = create_random_identity_provider()
    stored_items = identity_provider.get_multi()
    assert len(stored_items) == 2

    stored_items = identity_provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = identity_provider.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].endpoint == item.endpoint

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = identity_provider.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = identity_provider.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    item_update = create_random_update_identity_provider_data()
    item2 = identity_provider.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.endpoint == item_update.endpoint

    item_update = create_random_update_identity_provider_data()
    item2 = identity_provider.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.endpoint == item_update.endpoint


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    item2 = identity_provider.remove(db_obj=item)
    item3 = identity_provider.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
