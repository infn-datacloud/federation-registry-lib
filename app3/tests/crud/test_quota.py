from typing import Generator

from ..utils.quota import create_random_quota
from ..utils.utils import random_lower_string, random_non_negative_float
from ...quota.crud import quota
from ...quota.schemas import QuotaCreate, QuotaUpdate


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


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_quota()
    description2 = random_lower_string()
    tot_limit2 = random_non_negative_float()
    instance_limit2 = random_non_negative_float()
    user_limit2 = random_non_negative_float()
    tot_guaranteed2 = random_non_negative_float()
    instance_guaranteed2 = random_non_negative_float()
    user_guaranteed2 = random_non_negative_float()
    item_update = QuotaUpdate(
        description=description2,
        tot_limit=tot_limit2,
        instance_limit=instance_limit2,
        user_limit=user_limit2,
        tot_guaranteed=tot_guaranteed2,
        instance_guaranteed=instance_guaranteed2,
        user_guaranteed=user_guaranteed2,
    )
    item2 = quota.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == description2
    assert item2.tot_limit == tot_limit2
    assert item2.instance_limit == instance_limit2
    assert item2.user_limit == user_limit2
    assert item2.tot_guaranteed == tot_guaranteed2
    assert item2.instance_guaranteed == instance_guaranteed2
    assert item2.user_guaranteed == user_guaranteed2


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_quota()
    item2 = quota.remove(db_obj=item)
    item3 = quota.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
