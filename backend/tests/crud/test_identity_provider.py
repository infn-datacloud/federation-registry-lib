from typing import Generator
from uuid import uuid4

from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.provider.crud import provider
from app.provider.models import Provider
from app.user_group.crud import user_group
from tests.utils.identity_provider import (
    create_random_identity_provider,
    create_random_identity_provider_patch,
    validate_create_identity_provider_attrs,
)


def test_create_item_with_projects(db_provider_with_single_project: Provider) -> None:
    """Create an Identity Provider accepted by a specific Provider with a User Group for
    each received project.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_single_project.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_single_project
    )
    validate_create_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values_with_projects(
    db_provider_with_single_project: Provider,
) -> None:
    """Create an Identity Provider, with default values when possible, accepted by a
    specific Provider with a User Group for each received project.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_single_project.projects]
    )
    item = identity_provider.create(
        obj_in=item_in, provider=db_provider_with_single_project
    )
    validate_create_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_idp_with_single_user_group: IdentityProvider) -> None:
    """Retrieve an Identity Provider from its UID."""
    item = identity_provider.get(uid=db_idp_with_single_user_group.uid)
    assert item.uid == db_idp_with_single_user_group.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing Identity Provider."""
    assert not identity_provider.get(uid=uuid4())


def test_get_items(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
) -> None:
    """Retrieve multiple Identity Providers."""
    stored_items = identity_provider.get_multi()
    assert len(stored_items) == 2

    stored_items = identity_provider.get_multi(uid=db_idp_with_single_user_group.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_idp_with_single_user_group.uid

    stored_items = identity_provider.get_multi(uid=db_idp_with_multiple_user_groups.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_idp_with_multiple_user_groups.uid


def test_get_items_with_limit(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = identity_provider.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = identity_provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = identity_provider.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = list(sorted(identity_provider.get_multi(), key=lambda x: x.uid))

    stored_items = identity_provider.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = identity_provider.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = identity_provider.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = identity_provider.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_idp_with_single_user_group: IdentityProvider) -> None:
    """Update the attributes of an existing Identity Provider, without updating its
    relationships.
    """
    patch_in = create_random_identity_provider_patch()
    item = identity_provider.update(
        db_obj=db_idp_with_single_user_group, obj_in=patch_in
    )
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
    """Try to update the attributes of an existing Identity Provider, without updating
    its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
    """
    patch_in = create_random_identity_provider_patch(default=True)
    assert not identity_provider.update(
        db_obj=db_idp_with_single_user_group, obj_in=patch_in
    )

    patch_in = create_random_identity_provider_patch(default=True)
    patch_in.description = ""
    item = identity_provider.update(
        db_obj=db_idp_with_single_user_group, obj_in=patch_in
    )
    assert item.description == patch_in.description
    for k, v in db_idp_with_single_user_group.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_forced_update_user_groups(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
    """Update the attributes and relationships of an existing Identity Provider.

    Update an Identity Provider with a set of linked User Groups, changing both its
    attributes and replacing the linked User Groups with new ones. Keep the relationship
    with the provider unchanged.
    """
    db_provider = db_idp_with_single_user_group.providers.single()
    db_user_group = db_idp_with_single_user_group.user_groups.single()
    rel = db_idp_with_single_user_group.providers.relationship(db_provider)
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects]
    )
    item_in.relationship.idp_name = rel.idp_name
    item_in.relationship.protocol = rel.protocol
    item = identity_provider.update(
        db_obj=db_idp_with_single_user_group,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_identity_provider_attrs(obj_in=item_in, db_item=item)
    assert item.providers.single() == db_provider
    assert item.providers.relationship(db_provider).protocol == rel.protocol
    assert item.providers.relationship(db_provider).idp_name == rel.idp_name
    assert item.user_groups.single() != db_user_group


def test_forced_update_item_without_changing_relationships(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
    """Update the attributes and relationships of an existing Identity Provider.

    Update an Identity Provider with a set of linked User Groups, changing only its
    attributes leaving untouched its connections (this is different from the previous
    test because the flag force is set to True).
    """
    db_provider = db_idp_with_single_user_group.providers.single()
    db_user_group = db_idp_with_single_user_group.user_groups.single()
    rel = db_idp_with_single_user_group.providers.relationship(db_provider)
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects]
    )
    item_in.user_groups[0].name = db_user_group.name
    item_in.relationship.idp_name = rel.idp_name
    item_in.relationship.protocol = rel.protocol
    item = identity_provider.update(
        db_obj=db_idp_with_single_user_group,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_identity_provider_attrs(obj_in=item_in, db_item=item)
    assert item.providers.single() == db_provider
    assert item.providers.relationship(db_provider).protocol == rel.protocol
    assert item.providers.relationship(db_provider).idp_name == rel.idp_name
    assert item.user_groups.single() == db_user_group


def test_forced_update_item_changing_provider_relationships_data(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
    """Update the attributes and relationships of an existing Identity Provider.

    Update an Identity Provider with a set of linked User Groups, changing only the
    attributes of the relationship with a target provider, leaving untouched the user
    groups.
    """
    db_provider = db_idp_with_single_user_group.providers.single()
    db_user_group = db_idp_with_single_user_group.user_groups.single()
    rel = db_idp_with_single_user_group.providers.relationship(db_provider)
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects]
    )
    item_in.user_groups[0].name = db_user_group.name
    item = identity_provider.update(
        db_obj=db_idp_with_single_user_group,
        obj_in=item_in,
        projects=db_provider.projects,
        provider=db_provider,
        force=True,
    )
    validate_create_identity_provider_attrs(obj_in=item_in, db_item=item)
    assert item.providers.single() == db_provider
    assert item.providers.relationship(db_provider).protocol != rel.protocol
    assert item.providers.relationship(db_provider).idp_name != rel.idp_name
    assert item.user_groups.single() == db_user_group


def test_delete_item_with_relationships(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
    """Delete an existing Identity Provider.

    On cascade delete linked User Groups.
    """
    db_provider = db_idp_with_single_user_group.providers.single()
    db_user_group = db_idp_with_single_user_group.user_groups.single()
    assert identity_provider.remove(db_obj=db_idp_with_single_user_group)
    assert not identity_provider.get(uid=db_idp_with_single_user_group.uid)
    assert not user_group.get(uid=db_user_group.uid)
    assert provider.get(uid=db_provider.uid)
