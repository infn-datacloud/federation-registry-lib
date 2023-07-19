from typing import Generator

from app.tests.utils.quota import create_random_quota, create_random_update_quota_data
from app.tests.utils.utils import random_lower_string, random_non_negative_float
from app.quota.crud import quota
from app.quota.schemas import QuotaCreate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    tot_limit = random_non_negative_float()
    instance_limit = random_non_negative_float()
    user_limit = random_non_negative_float()
    tot_guaranteed = random_non_negative_float()
    instance_guaranteed = random_non_negative_float()
    user_guaranteed = random_non_negative_float()
    item_in = QuotaCreate(
        description=description,
        tot_limit=tot_limit,
        instance_limit=instance_limit,
        user_limit=user_limit,
        tot_guaranteed=tot_guaranteed,
        instance_guaranteed=instance_guaranteed,
        user_guaranteed=user_guaranteed,
    )
    item = quota.create(obj_in=item_in)
    assert item.description == description
    assert item.tot_limit == tot_limit
    assert item.instance_limit == instance_limit
    assert item.user_limit == user_limit
    assert item.tot_guaranteed == tot_guaranteed
    assert item.instance_guaranteed == instance_guaranteed
    assert item.user_guaranteed == user_guaranteed


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    item_in = QuotaCreate()
    item = quota.create(obj_in=item_in)
    assert item.description == ""
    assert item.tot_limit is None
    assert item.instance_limit is None
    assert item.user_limit is None
    assert item.tot_guaranteed == 0
    assert item.instance_guaranteed == 0
    assert item.user_guaranteed == 0


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_quota()
    stored_item = quota.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.tot_limit == stored_item.tot_limit
    assert item.instance_limit == stored_item.instance_limit
    assert item.user_limit == stored_item.user_limit
    assert item.tot_guaranteed == stored_item.tot_guaranteed
    assert item.instance_guaranteed == stored_item.instance_guaranteed
    assert item.user_guaranteed == stored_item.user_guaranteed


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_quota()
    item2 = create_random_quota()
    stored_items = quota.get_multi()
    assert len(stored_items) == 2

    stored_items = quota.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = quota.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].tot_limit == item.tot_limit
    assert stored_items[0].instance_limit == item.instance_limit
    assert stored_items[0].user_limit == item.user_limit
    assert stored_items[0].tot_guaranteed == item.tot_guaranteed
    assert stored_items[0].instance_guaranteed == item.instance_guaranteed
    assert stored_items[0].user_guaranteed == item.user_guaranteed

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = quota.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = quota.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_quota()
    item_update = create_random_update_quota_data()
    item2 = quota.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.tot_limit == item_update.tot_limit
    assert item2.instance_limit == item_update.instance_limit
    assert item2.user_limit == item_update.user_limit
    assert item2.tot_guaranteed == item_update.tot_guaranteed
    assert item2.instance_guaranteed == item_update.instance_guaranteed
    assert item2.user_guaranteed == item_update.user_guaranteed

    item_update = create_random_update_quota_data()
    item2 = quota.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.tot_limit == item_update.tot_limit
    assert item2.instance_limit == item_update.instance_limit
    assert item2.user_limit == item_update.user_limit
    assert item2.tot_guaranteed == item_update.tot_guaranteed
    assert item2.instance_guaranteed == item_update.instance_guaranteed
    assert item2.user_guaranteed == item_update.user_guaranteed


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_quota()
    item2 = quota.remove(db_obj=item)
    item3 = quota.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
