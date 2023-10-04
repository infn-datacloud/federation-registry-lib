from typing import Generator

from app.provider.crud import provider
from app.tests.utils.provider import create_random_provider, validate_provider_attrs


def test_create_item(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(default=True)
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(with_projects=True)
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_identity_providers(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_regions(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_everything(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(
        with_projects=True, with_identity_providers=True, with_regions=True
    )
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item = provider.get(uid=item.uid)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item_in2 = create_random_provider()
    item2 = provider.create(obj_in=item_in2)

    stored_items = provider.get_multi()
    assert len(stored_items) == 2

    stored_items = provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = provider.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_provider_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = provider.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_provider_attrs(obj_in=item_in2, db_item=stored_items[0])

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = provider.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = provider.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


# def test_update_item(setup_and_teardown_db: Generator) -> None:
#     item = create_random_provider()
#     item_update = create_random_update_provider_data()
#     item2 = provider.update(db_obj=item, obj_in=item_update)
#     assert item2.uid == item.uid
#     assert item.description == item_update.description
#     assert item.name == item_update.name
#     assert item.is_public == item_update.is_public
#     assert item.support_emails == item_update.support_emails

#     item_update = create_random_update_provider_data()
#     item2 = provider.update(db_obj=item, obj_in=item_update.dict())
#     assert item2.uid == item.uid
#     assert item.description == item_update.description
#     assert item.name == item_update.name
#     assert item.is_public == item_update.is_public
#     assert item.support_emails == item_update.support_emails


# def test_delete_item(setup_and_teardown_db: Generator) -> None:
#     item_in = create_random_provider()
#     item = provider.create(obj_in=item_in)
#     result = provider.remove(db_obj=item)
#     item = provider.get(uid=item.uid)
#     assert result is True
#     assert item is None
