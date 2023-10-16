from uuid import uuid4

from app.identity_provider.models import IdentityProvider
from app.project.crud import project
from app.tests.utils.project import create_random_project
from app.tests.utils.user_group import (
    create_random_user_group,
    validate_user_group_attrs,
)
from app.user_group.crud import user_group


def test_create_item(db_idp: IdentityProvider) -> None:
    """Create a User Group belonging to a specific Identity Provider with no
    assigned SLA."""
    item_in = create_random_user_group()
    item = user_group.create(obj_in=item_in, identity_provider=db_idp)
    validate_user_group_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_idp: IdentityProvider) -> None:
    """Create a User Group, with default values when possible,  belonging to a
    specific Identity Provider with no assigned SLA."""
    item_in = create_random_user_group(default=True)
    item = user_group.create(obj_in=item_in, identity_provider=db_idp)
    validate_user_group_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects(db_idp: IdentityProvider) -> None:
    """Create a User Group belonging to a specific Identity Provider with an
    assigned SLA for each received project."""
    provider = db_idp.providers.all()[0]
    item_in = create_random_user_group(projects=[i.uuid for i in provider.projects])
    item = user_group.create(
        obj_in=item_in, identity_provider=db_idp, projects=provider.projects
    )
    validate_user_group_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_idp: IdentityProvider) -> None:
    """Retrieve a User Group from its UID."""
    provider = db_idp.providers.all()[0]
    item_in = create_random_user_group(projects=[i.uuid for i in provider.projects])
    item = user_group.create(
        obj_in=item_in, identity_provider=db_idp, projects=provider.projects
    )
    item = user_group.get(uid=item.uid)
    validate_user_group_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_idp: IdentityProvider) -> None:
    """Try to retrieve a not existing User Group."""
    provider = db_idp.providers.all()[0]
    item_in = create_random_user_group(projects=[i.uuid for i in provider.projects])
    item = user_group.create(
        obj_in=item_in, identity_provider=db_idp, projects=provider.projects
    )
    item = user_group.get(uid=uuid4())
    assert not item


def test_get_items(db_idp: IdentityProvider) -> None:
    """Retrieve multiple User Groups.

    Filter GET operations specifying a target uid.
    """
    provider = db_idp.providers.all()[0]
    item_in = create_random_user_group(projects=[i.uuid for i in provider.projects])
    item = user_group.create(
        obj_in=item_in, identity_provider=db_idp, projects=provider.projects
    )
    item_in2 = create_random_user_group(projects=[i.uuid for i in provider.projects])
    item2 = user_group.create(
        obj_in=item_in2, identity_provider=db_idp, projects=provider.projects
    )
    stored_items = user_group.get_multi()
    assert len(stored_items) == 2

    stored_items = user_group.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_user_group_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = user_group.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_user_group_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_idp: IdentityProvider) -> None:
    """Test the 'limit' attribute in GET operations."""
    provider = db_idp.providers.all()[0]
    item_in = create_random_user_group(projects=[i.uuid for i in provider.projects])
    user_group.create(
        obj_in=item_in, identity_provider=db_idp, projects=provider.projects
    )
    item_in2 = create_random_user_group(projects=[i.uuid for i in provider.projects])
    user_group.create(
        obj_in=item_in2, identity_provider=db_idp, projects=provider.projects
    )

    stored_items = user_group.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = user_group.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = user_group.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_idp: IdentityProvider) -> None:
    """Test the 'sort' attribute in GET operations."""
    provider = db_idp.providers.all()[0]
    item_in = create_random_user_group(projects=[i.uuid for i in provider.projects])
    item = user_group.create(
        obj_in=item_in, identity_provider=db_idp, projects=provider.projects
    )
    item_in2 = create_random_user_group(projects=[i.uuid for i in provider.projects])
    item2 = user_group.create(
        obj_in=item_in2, identity_provider=db_idp, projects=provider.projects
    )

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = user_group.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = user_group.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_idp: IdentityProvider) -> None:
    """Test the 'skip' attribute in GET operations."""
    provider = db_idp.providers.all()[0]
    item_in = create_random_user_group(projects=[i.uuid for i in provider.projects])
    user_group.create(
        obj_in=item_in, identity_provider=db_idp, projects=provider.projects
    )
    item_in2 = create_random_user_group(projects=[i.uuid for i in provider.projects])
    user_group.create(
        obj_in=item_in2, identity_provider=db_idp, projects=provider.projects
    )

    stored_items = user_group.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = user_group.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_idp: IdentityProvider) -> None:
    """Update the attributes of an existing User Group.

    Do not update linked SLAs and identity provider.
    """
    item_in = create_random_user_group()
    item = user_group.create(obj_in=item_in, identity_provider=db_idp)
    item_in = create_random_user_group()
    item = user_group.update(db_obj=item, obj_in=item_in)
    validate_user_group_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_slas(db_idp: IdentityProvider) -> None:
    """Update the attributes and relationships of an existing User Group.

    At first update a User Group with a set of linked SLAs, updating its
    attributes and removing all linked SLAs.

    Update a User Group with no SLAs, changing its attributes and
    linking a new SLA.

    Update a User Group with a set of linked SLAs, changing both its
    attributes and replacing the linked SLAs with new ones.

    Update a User Group with a set of linked SLAs, changing only its
    attributes leaving untouched its connections (this is different from
    the previous test because the flag force is set to True).
    """
    db_provider = db_idp.providers.all()[0]
    db_project = db_provider.projects.all()[0]
    item_in = create_random_user_group(projects=[db_project.uuid])
    item = user_group.create(obj_in=item_in, identity_provider=db_idp)
    item_in = create_random_user_group()
    item = user_group.update(db_obj=item, obj_in=item_in, force=True)
    validate_user_group_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_user_group(projects=[db_project.uuid])
    item = user_group.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_user_group_attrs(obj_in=item_in, db_item=item)

    project_in = create_random_project()
    db_project = project.create(obj_in=project_in, provider=db_provider)
    item_in = create_random_user_group(projects=[db_project.uuid])
    item = user_group.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_user_group_attrs(obj_in=item_in, db_item=item)

    slas = item_in.slas
    item_in = create_random_user_group()
    item_in.slas = slas
    item = user_group.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_user_group_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_idp: IdentityProvider) -> None:
    """Delete an existing User Group with no SLAs."""
    item_in = create_random_user_group()
    item = user_group.create(obj_in=item_in, identity_provider=db_idp)
    result = user_group.remove(db_obj=item)
    assert result
    item = user_group.get(uid=item.uid)
    assert not item


def test_delete_item_with_relationships(db_idp: IdentityProvider) -> None:
    """Delete an existing User Group.

    On cascade delete linked SLAs.
    """
    provider = db_idp.providers.all()[0]
    item_in = create_random_user_group(
        projects=[i.uuid for i in provider.projects],
    )
    item = user_group.create(
        obj_in=item_in, identity_provider=db_idp, projects=provider.projects
    )
    result = user_group.remove(db_obj=item)
    assert result
    item = user_group.get(uid=item.uid)
    assert not item
