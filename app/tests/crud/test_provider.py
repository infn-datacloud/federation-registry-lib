from typing import Generator

from app.tests.utils.provider import (
    create_random_provider,
    create_random_update_provider_data,
)
from app.tests.utils.utils import (
    random_bool,
    random_email,
    random_lower_string,
)
from app.provider.crud import provider
from app.provider.schemas import ProviderCreate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    name = random_lower_string()
    is_public = random_bool()
    support_emails = [random_email()]
    item_in = ProviderCreate(
        description=description,
        name=name,
        is_public=is_public,
        support_emails=support_emails,
    )
    item = provider.create(obj_in=item_in)
    assert item.description == description
    assert item.name == name
    assert item.is_public == is_public
    assert item.support_emails == support_emails


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    item_in = ProviderCreate(name=name)
    item = provider.create(obj_in=item_in)
    assert item.description == ""
    assert item.name == name
    assert item.is_public is False
    assert item.support_emails == []


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_provider()
    stored_item = provider.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.name == stored_item.name
    assert item.is_public == stored_item.is_public
    assert item.support_emails == stored_item.support_emails


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_provider()
    item2 = create_random_provider()
    stored_items = provider.get_multi()
    assert len(stored_items) == 2

    stored_items = provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = provider.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].name == item.name
    assert stored_items[0].is_public == item.is_public
    assert stored_items[0].support_emails == item.support_emails

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = provider.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = provider.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_provider()
    item_update = create_random_update_provider_data()
    item2 = provider.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item.description == item_update.description
    assert item.name == item_update.name
    assert item.is_public == item_update.is_public
    assert item.support_emails == item_update.support_emails

    item_update = create_random_update_provider_data()
    item2 = provider.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item.description == item_update.description
    assert item.name == item_update.name
    assert item.is_public == item_update.is_public
    assert item.support_emails == item_update.support_emails


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_provider()
    item2 = provider.remove(db_obj=item)
    item3 = provider.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
