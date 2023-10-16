from uuid import uuid4

from app.identity_provider.crud import identity_provider
from app.project.crud import project
from app.provider.models import Provider
from app.tests.utils.identity_provider import (
    create_random_identity_provider,
    create_random_update_identity_provider,
    validate_identity_provider_attrs,
)
from app.tests.utils.project import create_random_project


def test_create_item(db_provider: Provider) -> None:
    """Create an Identity Provider accepted by a specific Provider with no
    assigned User Groups."""
    item_in = create_random_identity_provider()
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_provider: Provider) -> None:
    """Create an Identity Provider, with default values when possible, accepted
    by a specific Provider with no assigned User Groups."""
    item_in = create_random_identity_provider(default=True)
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects(db_provider: Provider) -> None:
    """Create an Identity Provider accepted by a specific Provider with a User
    Group for each received project."""
    proj = create_random_project()
    project.create(obj_in=proj, provider=db_provider)
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_provider: Provider) -> None:
    """Retrieve an Identity Provider from its UID."""
    item_in = create_random_identity_provider()
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    item = identity_provider.get(uid=item.uid)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_provider: Provider) -> None:
    """Try to retrieve a not existing Identity Provider."""
    item_in = create_random_identity_provider()
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    item = identity_provider.get(uid=uuid4())
    assert not item


def test_get_items(db_provider: Provider) -> None:
    """Retrieve multiple User Groups.

    Filter GET operations specifying a target uid.
    """
    item_in = create_random_identity_provider()
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_identity_provider()
    item2 = identity_provider.create(obj_in=item_in2, provider=db_provider)

    stored_items = identity_provider.get_multi()
    assert len(stored_items) == 2

    stored_items = identity_provider.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_identity_provider_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = identity_provider.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_identity_provider_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_provider: Provider) -> None:
    """Test the 'limit' attribute in GET operations."""
    item_in = create_random_identity_provider()
    identity_provider.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_identity_provider()
    identity_provider.create(obj_in=item_in2, provider=db_provider)

    stored_items = identity_provider.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = identity_provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = identity_provider.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_provider: Provider) -> None:
    """Test the 'sort' attribute in GET operations."""
    item_in = create_random_identity_provider()
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_identity_provider()
    item2 = identity_provider.create(obj_in=item_in2, provider=db_provider)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = identity_provider.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = identity_provider.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_provider: Provider) -> None:
    """Test the 'skip' attribute in GET operations."""
    item_in = create_random_identity_provider()
    identity_provider.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_identity_provider()
    identity_provider.create(obj_in=item_in2, provider=db_provider)

    stored_items = identity_provider.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = identity_provider.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_provider: Provider) -> None:
    """Update the attributes of an existing Identity Provider.

    Do not update linked User Groups and Providers.
    """
    item_in = create_random_identity_provider()
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_update_identity_provider()
    item = identity_provider.update(db_obj=item, obj_in=item_in)

    assert item.description == item_in.description
    assert item.endpoint == item_in.endpoint
    assert item.group_claim == item_in.group_claim


def test_forced_update_item_with_projects_and_user_groups(
    db_provider: Provider,
) -> None:
    """Update the attributes and relationships of an existing Identity
    Provider.

    At first update an Identity Provider with a set of linked User
    Groups, updating its attributes and removing all linked User Groups.

    Update an Identity Provider with no User Groups, changing its
    attributes and linking a new User Group.

    Update an Identity Provider with a set of linked User Groups,
    changing both its attributes and replacing the linked User Groups
    with new ones.

    Update an Identity Provider with a set of linked User Groups,
    changing only its attributes leaving untouched its connections (this
    is different from the previous test because the flag force is set to
    True).

    Update an Identity Provider with a set of linked User Groups,
    changing only the attributes of the relationship with a target
    provider, leaving untouched the user groups.
    """
    proj = create_random_project()
    project.create(obj_in=proj, provider=db_provider)
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider)

    auth_data = item_in.relationship
    item_in = create_random_identity_provider()
    item_in.relationship = auth_data
    item = identity_provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)

    auth_data = item_in.relationship
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects]
    )
    item_in.relationship = auth_data

    item = identity_provider.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)

    auth_data = item_in.relationship
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects]
    )
    item_in.relationship = auth_data
    item = identity_provider.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)

    auth_data = item_in.relationship
    user_groups = item_in.user_groups
    item_in = create_random_identity_provider()
    item_in.user_groups = user_groups
    item_in.relationship = auth_data
    item = identity_provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)

    user_groups = item_in.user_groups
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects]
    )
    item_in.user_groups = user_groups
    item = identity_provider.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider.projects,
        provider=db_provider,
        force=True,
    )
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_provider: Provider) -> None:
    """Delete an existing Identity Provider with no SLAs."""
    item_in = create_random_identity_provider()
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    result = identity_provider.remove(db_obj=item)
    assert result
    item = identity_provider.get(uid=item.uid)
    assert not item


def test_delete_item_with_relationships(db_provider: Provider) -> None:
    """Delete an existing Identity Provider.

    On cascade delete linked User Groups.
    """
    proj = create_random_project()
    project.create(obj_in=proj, provider=db_provider)
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider.projects],
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider)
    result = identity_provider.remove(db_obj=item)
    assert result
    item = identity_provider.get(uid=item.uid)
    assert not item
