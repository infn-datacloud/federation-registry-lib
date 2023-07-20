from typing import Generator
from app.user_group.crud import user_group
from app.user_group.schemas import UserGroupCreate
from app.tests.utils.identity_provider import create_random_identity_provider
from app.tests.utils.user_group import (
    create_random_update_user_group_data,
    create_random_user_group,
)
from app.tests.utils.utils import random_lower_string


def test_create_item(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    description = random_lower_string()
    item_in = UserGroupCreate(name=name, description=description)
    item = user_group.create(
        obj_in=item_in, identity_provider=create_random_identity_provider()
    )
    assert item.name == name
    assert item.description == description


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    item_in = UserGroupCreate(name=name)
    item = user_group.create(
        obj_in=item_in, identity_provider=create_random_identity_provider()
    )
    assert item.name == name
    assert item.description == ""


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_user_group()
    stored_item = user_group.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.name == stored_item.name
    assert item.description == stored_item.description


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_user_group()
    item2 = create_random_user_group()
    stored_items = user_group.get_multi()
    assert len(stored_items) == 2

    stored_items = user_group.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = user_group.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].name == item.name
    assert stored_items[0].description == item.description

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = user_group.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = user_group.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_user_group()
    item_update = create_random_update_user_group_data()
    item2 = user_group.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.name == item_update.name
    assert item2.description == item_update.description

    item_update = create_random_update_user_group_data()
    item2 = user_group.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.name == item_update.name
    assert item2.description == item_update.description


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_user_group()
    item2 = user_group.remove(db_obj=item)
    item3 = user_group.get(uid=item.uid)
    assert item2 is True
    assert item3 is None


# TODO
# Presence of UniqueIdProperty creates a new instance
# with same name but different UUID. The following test fails
#
# def test_create_item_duplicate_name(setup_and_teardown_db) -> None:
#    name = random_lower_string()
#    description = random_lower_string()
#    item_in = UserGroupCreate(name=name, description=description)
#    item = user_group.create(obj_in=item_in)
#    assert item.name == name
#    assert item.description == description
#
#    item_in = UserGroupCreate(name=name)
#    item2 = user_group.create(obj_in=item_in)
#    assert item2.uid == item.uid
#    assert item2.name == item.name
#    assert item2.description == item.description
