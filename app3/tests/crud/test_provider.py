from typing import Generator

from ..utils.provider import create_random_provider
from ..utils.utils import random_bool, random_email, random_lower_string
from ...provider.crud import provider
from ...provider.schemas import ProviderCreate, ProviderUpdate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    name = random_lower_string()
    is_public = random_bool()
    support_email = [random_email()]
    item_in = ProviderCreate(
        description=description,
        name=name,
        is_public=is_public,
        support_email=support_email,
    )
    item = provider.create(obj_in=item_in)
    assert item.description == description
    assert item.name == name
    assert item.is_public == is_public
    assert item.support_email == support_email


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    item_in = ProviderCreate(name=name)
    item = provider.create(obj_in=item_in)
    assert item.description == ""
    assert item.name == name
    assert item.is_public is False
    assert item.support_email == []


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_provider()
    stored_item = provider.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.name == stored_item.name
    assert item.is_public == stored_item.is_public
    assert item.support_email == stored_item.support_email


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_provider()
    description2 = random_lower_string()
    name2 = random_lower_string()
    is_public2 = not item.is_public
    support_email2 = [random_email()]
    item_update = ProviderUpdate(
        description=description2,
        name=name2,
        is_public=is_public2,
        support_email=support_email2,
    )
    item2 = provider.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item.description == description2
    assert item.name == name2
    assert item.is_public == is_public2
    assert item.support_email == support_email2


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_provider()
    item2 = provider.remove(db_obj=item)
    item3 = provider.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
