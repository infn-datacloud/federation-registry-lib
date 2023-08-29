from typing import Generator

from app.auth_method.schemas import AuthMethodCreate
from app.identity_provider.crud import identity_provider
from app.identity_provider.schemas import IdentityProviderCreate
from app.tests.utils.identity_provider import (
    create_random_identity_provider,
    create_random_update_identity_provider_data,
)
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import random_lower_string, random_url


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    endpoint = random_url()
    group_claim = random_lower_string()
    item_in = IdentityProviderCreate(
        description=description, endpoint=endpoint, group_claim=group_claim
    )
    item = identity_provider.create(obj_in=item_in)
    assert item.description == description
    assert item.endpoint == endpoint
    assert item.group_claim == group_claim


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    endpoint = random_url()
    group_claim = random_lower_string()
    item_in = IdentityProviderCreate(
        endpoint=endpoint, group_claim=group_claim
    )
    item = identity_provider.create(obj_in=item_in)
    assert item.description == ""
    assert item.endpoint == endpoint
    assert item.group_claim == group_claim


def test_create_item_with_provider(setup_and_teardown_db: Generator) -> None:
    endpoint = random_url()
    group_claim = random_lower_string()
    item_in = IdentityProviderCreate(
        endpoint=endpoint, group_claim=group_claim
    )
    provider = create_random_provider()
    idp_name = random_lower_string()
    protocol = random_lower_string()
    auth_method = AuthMethodCreate(idp_name=idp_name, protocol=protocol)
    item = identity_provider.create(
        obj_in=item_in, provider=provider, relationship=auth_method
    )
    assert item.description == ""
    assert item.endpoint == endpoint
    assert item.group_claim == group_claim
    item_providers = item.providers.all()
    assert len(item_providers) == 1
    assert item_providers[0].uid == provider.uid
    assert (
        item.providers.relationship(provider).idp_name == auth_method.idp_name
    )
    assert (
        item.providers.relationship(provider).protocol == auth_method.protocol
    )


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    stored_item = identity_provider.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.endpoint == stored_item.endpoint
    assert item.group_claim == stored_item.group_claim

    stored_item = identity_provider.get(endpoint=item.endpoint)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.endpoint == stored_item.endpoint
    assert item.group_claim == stored_item.group_claim


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    item2 = create_random_identity_provider()
    stored_items = identity_provider.get_multi()
    assert len(stored_items) == 2

    stored_items = identity_provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = identity_provider.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].endpoint == item.endpoint
    assert stored_items[0].group_claim == item.group_claim

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = identity_provider.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = identity_provider.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    item_update = create_random_update_identity_provider_data()
    item2 = identity_provider.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.endpoint == item_update.endpoint

    item_update = create_random_update_identity_provider_data()
    item2 = identity_provider.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.endpoint == item_update.endpoint


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_identity_provider()
    item2 = identity_provider.remove(db_obj=item)
    item3 = identity_provider.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
