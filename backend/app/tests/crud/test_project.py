from uuid import uuid4

from app.project.crud import project
from app.provider.models import Provider
from app.tests.utils.project import create_random_project, validate_project_attrs


def test_create_item(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    validate_project_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_provider: Provider) -> None:
    item_in = create_random_project(default=True)
    item = project.create(obj_in=item_in, provider=db_provider)
    validate_project_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item = project.get(uid=item.uid)
    validate_project_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item = project.get(uid=uuid4())
    assert not item


def test_get_items(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_project()
    item2 = project.create(obj_in=item_in2, provider=db_provider)

    stored_items = project.get_multi()
    assert len(stored_items) == 2

    stored_items = project.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_project_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = project.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_project_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_provider: Provider) -> None:
    item_in = create_random_project()
    project.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_project()
    project.create(obj_in=item_in2, provider=db_provider)

    stored_items = project.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = project.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = project.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_project()
    item2 = project.create(obj_in=item_in2, provider=db_provider)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = project.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = project.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_provider: Provider) -> None:
    item_in = create_random_project()
    project.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_project()
    project.create(obj_in=item_in2, provider=db_provider)

    stored_items = project.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = project.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_project()
    item = project.update(db_obj=item, obj_in=item_in)
    validate_project_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_project()
    item = project.update(db_obj=item, obj_in=item_in, force=True)
    validate_project_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    result = project.remove(db_obj=item)
    assert result
    item = project.get(uid=item.uid)
    assert not item
