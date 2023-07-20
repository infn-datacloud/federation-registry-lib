from typing import Generator
from uuid import uuid4
from app.sla.crud import sla
from app.sla.schemas import SLACreate
from app.tests.utils.project import create_random_project
from app.tests.utils.sla import (
    create_random_sla,
    create_random_update_sla_data,
)
from app.tests.utils.user_group import create_random_user_group
from app.tests.utils.utils import random_lower_string, random_datetime


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    start_date = random_datetime()
    end_date = random_datetime()
    document_uuid = uuid4()
    item_in = SLACreate(
        description=description,
        start_date=start_date,
        end_date=end_date,
        document_uuid=document_uuid,
    )
    item = sla.create(
        obj_in=item_in,
        project=create_random_project(),
        user_group=create_random_user_group(),
    )
    assert item.description == description
    assert item.start_date == start_date
    assert item.end_date == end_date
    assert item.document_uuid == str(document_uuid)


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    start_date = random_datetime()
    item_in = SLACreate(start_date=start_date)
    item = sla.create(
        obj_in=item_in,
        project=create_random_project(),
        user_group=create_random_user_group(),
    )
    assert item.description == ""
    assert item.start_date == start_date
    assert item.end_date is None
    assert item.document_uuid is None


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_sla()
    stored_item = sla.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.start_date == stored_item.start_date
    assert item.end_date == stored_item.end_date
    assert item.document_uuid == stored_item.document_uuid


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_sla()
    item2 = create_random_sla()
    stored_items = sla.get_multi()
    assert len(stored_items) == 2

    stored_items = sla.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = sla.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].start_date == item.start_date
    assert stored_items[0].end_date == item.end_date
    assert stored_items[0].document_uuid == item.document_uuid

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = sla.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = sla.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_sla()
    item_update = create_random_update_sla_data()
    item2 = sla.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.start_date == item_update.start_date
    assert item2.end_date == item_update.end_date

    item_update = create_random_update_sla_data()
    item2 = sla.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.start_date == item_update.start_date
    assert item2.end_date == item_update.end_date


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_sla()
    item2 = sla.remove(db_obj=item)
    item3 = sla.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
