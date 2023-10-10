from uuid import uuid4

from app.location.crud import location
from app.region.models import Region
from app.tests.utils.location import create_random_location, validate_location_attrs


def test_create_item(db_region: Region) -> None:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    validate_location_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_region: Region) -> None:
    item_in = create_random_location(default=True)
    item = location.create(obj_in=item_in, region=db_region)
    validate_location_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_region: Region) -> None:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    item = location.get(uid=item.uid)
    validate_location_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_region: Region) -> None:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    item = location.get(uid=uuid4())
    assert not item


def test_get_items(db_region: Region) -> None:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_location()
    item2 = location.create(obj_in=item_in2, region=db_region)

    stored_items = location.get_multi()
    assert len(stored_items) == 2

    stored_items = location.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_location_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = location.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_location_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_region: Region) -> None:
    item_in = create_random_location()
    location.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_location()
    location.create(obj_in=item_in2, region=db_region)

    stored_items = location.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = location.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = location.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_region: Region) -> None:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_location()
    item2 = location.create(obj_in=item_in2, region=db_region)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = location.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = location.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_region: Region) -> None:
    item_in = create_random_location()
    location.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_location()
    location.create(obj_in=item_in2, region=db_region)

    stored_items = location.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = location.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_region: Region) -> None:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    item_in = create_random_location()
    item = location.update(db_obj=item, obj_in=item_in)
    validate_location_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item(db_region: Region) -> None:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    item_in = create_random_location()
    item = location.update(db_obj=item, obj_in=item_in, force=True)
    validate_location_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_region: Region) -> None:
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    result = location.remove(db_obj=item)
    assert result
    item = location.get(uid=item.uid)
    assert not item
