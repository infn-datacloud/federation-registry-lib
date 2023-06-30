from typing import Generator

from ..utils.identity_provider import create_random_identity_provider
from ..utils.utils import random_lower_string, random_url
from ...identity_provider.crud import identity_provider
from ...identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderUpdate,
)


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


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    description2 = random_lower_string()
    endpoint2 = random_url()
    item_update = IdentityProviderUpdate(
        description=description2, endpoint=endpoint2
    )
    item2 = identity_provider.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == description2
    assert item2.endpoint == endpoint2


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    item2 = identity_provider.remove(db_obj=item)
    item3 = identity_provider.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
