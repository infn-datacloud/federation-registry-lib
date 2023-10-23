from uuid import uuid4

from app.identity_provider.crud import identity_provider
from app.project.crud import project
from app.provider.models import Provider
from app.tests.utils.identity_provider import (
    create_random_identity_provider,
    create_random_identity_provider_patch,
    validate_identity_provider_attrs,
)
from app.tests.utils.project import create_random_project
from app.user_group.crud import user_group


def test_create_item_with_projects(db_provider_with_project: Provider) -> None:
    """Create an Identity Provider accepted by a specific Provider with a User
    Group for each received project."""
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values_with_projects(
    db_provider_with_project: Provider,
) -> None:
    """Create an Identity Provider, with default values when possible, accepted
    by a specific Provider with a User Group for each received project."""
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_provider_with_project: Provider) -> None:
    """Retrieve an Identity Provider from its UID."""
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    item = identity_provider.get(uid=item.uid)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_provider_with_project: Provider) -> None:
    """Try to retrieve a not existing Identity Provider."""
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    item = identity_provider.get(uid=uuid4())
    assert not item


def test_get_items(db_provider_with_project: Provider) -> None:
    """Retrieve multiple Identity Providers."""
    db_project1 = db_provider_with_project.projects.all()[0]
    db_project2 = project.create(
        obj_in=create_random_project(), provider=db_provider_with_project
    )
    item_in = create_random_identity_provider(projects=[db_project1.uuid])
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    item_in2 = create_random_identity_provider(projects=[db_project2.uuid])
    item2 = identity_provider.create(obj_in=item_in2, provider=db_provider_with_project)

    stored_items = identity_provider.get_multi()
    assert len(stored_items) == 2

    stored_items = identity_provider.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_identity_provider_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = identity_provider.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_identity_provider_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_provider_with_project: Provider) -> None:
    """Test the 'limit' attribute in GET operations."""
    db_project1 = db_provider_with_project.projects.all()[0]
    db_project2 = project.create(
        obj_in=create_random_project(), provider=db_provider_with_project
    )
    item_in = create_random_identity_provider(projects=[db_project1.uuid])
    identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    item_in2 = create_random_identity_provider(projects=[db_project2.uuid])
    identity_provider.create(obj_in=item_in2, provider=db_provider_with_project)

    stored_items = identity_provider.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = identity_provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = identity_provider.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_provider_with_project: Provider) -> None:
    """Test the 'sort' attribute in GET operations."""
    db_project1 = db_provider_with_project.projects.all()[0]
    db_project2 = project.create(
        obj_in=create_random_project(), provider=db_provider_with_project
    )
    item_in = create_random_identity_provider(projects=[db_project1.uuid])
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    item_in2 = create_random_identity_provider(projects=[db_project2.uuid])
    item2 = identity_provider.create(obj_in=item_in2, provider=db_provider_with_project)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = identity_provider.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = identity_provider.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_provider_with_project: Provider) -> None:
    """Test the 'skip' attribute in GET operations."""
    db_project1 = db_provider_with_project.projects.all()[0]
    db_project2 = project.create(
        obj_in=create_random_project(), provider=db_provider_with_project
    )
    item_in = create_random_identity_provider(projects=[db_project1.uuid])
    identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    item_in2 = create_random_identity_provider(projects=[db_project2.uuid])
    identity_provider.create(obj_in=item_in2, provider=db_provider_with_project)

    stored_items = identity_provider.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = identity_provider.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_provider_with_project: Provider) -> None:
    """Update the attributes of an existing Identity Provider, without updating
    its relationships."""
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    patch_in = create_random_identity_provider_patch()
    item = identity_provider.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_provider_with_project: Provider) -> None:
    """Try to update the attributes of an existing Identity Provider, without
    updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    patch_in = create_random_identity_provider_patch(default=True)
    assert not identity_provider.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_identity_provider_patch(default=True)
    patch_in.description = ""
    item = identity_provider.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_user_groups(
    db_provider_with_project: Provider,
) -> None:
    """Update the attributes and relationships of an existing Identity
    Provider.

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
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)

    auth_data = item_in.relationship
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item_in.relationship = auth_data
    item = identity_provider.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_project.projects,
        force=True,
    )
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)

    auth_data = item_in.relationship
    user_groups = item_in.user_groups
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item_in.user_groups = user_groups
    item_in.relationship = auth_data
    item = identity_provider.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_project.projects,
        force=True,
    )
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)

    user_groups = item_in.user_groups
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects]
    )
    item_in.user_groups = user_groups
    item = identity_provider.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_project.projects,
        provider=db_provider_with_project,
        force=True,
    )
    validate_identity_provider_attrs(obj_in=item_in, db_item=item)


def test_delete_item_with_relationships(db_provider_with_project: Provider) -> None:
    """Delete an existing Identity Provider.

    On cascade delete linked User Groups.
    """
    item_in = create_random_identity_provider(
        projects=[i.uuid for i in db_provider_with_project.projects],
    )
    item = identity_provider.create(obj_in=item_in, provider=db_provider_with_project)
    result = identity_provider.remove(db_obj=item)
    assert result
    item = identity_provider.get(uid=item.uid)
    assert not item
    assert not len(user_group.get_multi())
