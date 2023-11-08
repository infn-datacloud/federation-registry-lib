from datetime import timedelta
from typing import Generator
from uuid import uuid4

from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.project.crud import project
from app.provider.models import Provider
from app.sla.crud import sla
from app.user_group.crud import user_group
from app.user_group.models import UserGroup
from tests.utils.project import create_random_project
from tests.utils.user_group import (
    create_random_user_group,
    create_random_user_group_patch,
    validate_create_user_group_attrs,
)


def test_create_item_with_projects(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
    """Create a User Group belonging to a specific Identity Provider.

    It has an SLA for each received project.
    """
    db_provider = db_idp_with_single_user_group.providers.single()
    db_project = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_user_group(project=db_project.uuid)
    item = user_group.create(
        obj_in=item_in,
        identity_provider=db_idp_with_single_user_group,
        projects=db_provider.projects,
    )
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values_with_projects(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
    """Create a User Group belonging to a specific Identity Provider.

    Set default values when possible.
    It has an SLA for each received project.
    """
    db_provider = db_idp_with_single_user_group.providers.single()
    db_project = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_user_group(project=db_project.uuid)
    item = user_group.create(
        obj_in=item_in,
        identity_provider=db_idp_with_single_user_group,
        projects=db_provider.projects,
    )
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_user_group: UserGroup) -> None:
    """Retrieve a User Group from its UID."""
    item = user_group.get(uid=db_user_group.uid)
    assert item.uid == db_user_group.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing User Group."""
    assert not user_group.get(uid=uuid4())


def test_get_items(db_user_group2: UserGroup, db_user_group3: UserGroup) -> None:
    """Retrieve multiple User Groups."""
    stored_items = user_group.get_multi()
    assert len(stored_items) == 2

    stored_items = user_group.get_multi(uid=db_user_group2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_user_group2.uid

    stored_items = user_group.get_multi(uid=db_user_group3.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_user_group3.uid


def test_get_items_with_limit(
    db_user_group2: UserGroup, db_user_group3: UserGroup
) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = user_group.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = user_group.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = user_group.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_user_group2: UserGroup, db_user_group3: UserGroup) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = sorted(user_group.get_multi(), key=lambda x: x.uid)

    stored_items = user_group.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = user_group.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(
    db_user_group2: UserGroup, db_user_group3: UserGroup
) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = user_group.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = user_group.get_multi(skip=1)
    assert len(stored_items) == 1


def test_get_items_with_from_idp_endpoint(db_user_group3: UserGroup) -> None:
    """Retrieve User Groups belonging to a specific provider."""
    db_idp = db_user_group3.identity_provider.single()
    stored_items = user_group.get_multi(sort="uid", endpoint=db_idp.endpoint)
    assert len(stored_items) == 2
    for i, j in zip(user_group.get_multi(sort="uid"), stored_items):
        assert i.uid == j.uid


def test_patch_item(db_user_group: UserGroup) -> None:
    """Update the attributes of an existing User Group.

    Do not update its relationships.
    """
    patch_in = create_random_user_group_patch()
    item = user_group.update(db_obj=db_user_group, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_user_group: UserGroup) -> None:
    """Try to update the attributes of an existing User Group with defaults.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds. Do not update its relationships.
    """
    patch_in = create_random_user_group_patch(default=True)
    assert not user_group.update(db_obj=db_user_group, obj_in=patch_in)

    patch_in = create_random_user_group_patch(default=True)
    patch_in.description = ""
    item = user_group.update(db_obj=db_user_group, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_user_group.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_force_update_without_changing_relationships(db_user_group: UserGroup) -> None:
    """Update the attributes of an existing User Group.

    Update a User Group with a set of linked SLAs, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_idp = db_user_group.identity_provider.single()
    db_slas = sorted(db_user_group.slas, key=lambda x: x.uid)
    db_sla = db_user_group.slas.single()
    db_project = db_sla.projects.single()
    db_provider = db_project.provider.single()
    item_in = create_random_user_group(project=db_project.uuid)
    item_in.sla.doc_uuid = db_sla.doc_uuid
    if db_sla.start_date >= item_in.sla.end_date:
        item_in.sla.end_date = db_sla.start_date + timedelta(1)
    item_in.sla.start_date = db_sla.start_date
    item_in.sla.end_date = db_sla.end_date
    item = user_group.update(
        db_obj=db_user_group, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)
    assert item.identity_provider.single() == db_idp
    for i, j in zip(sorted(item.slas, key=lambda x: x.uid), db_slas):
        assert i == j


def test_replace_sla_with_another_same_provider(db_user_group: UserGroup) -> None:
    """Update the attributes and relationships of an existing User Group.

    Update a User Group with a set of linked SLAs, changing both its attributes and
    replacing the linked SLAs with new ones.
    """
    db_sla = db_user_group.slas.single()
    db_project = db_sla.projects.single()
    db_provider = db_project.provider.single()
    item_in = create_random_user_group(project=db_project.uuid)
    item = user_group.update(
        db_obj=db_user_group, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)


def test_add_new_sla_diff_provider_to_existing_user_group(
    db_user_group: UserGroup, db_provider_with_multiple_projects: Provider
) -> None:
    """Add new SLA to User Group.

    Update an existing User Group with a single SLA adding a new SLA belonging to
    another provider.
    """
    db_project = db_provider_with_multiple_projects.projects.single()
    item_in = create_random_user_group(project=db_project.uuid)
    item_in.name = db_user_group.name
    item = user_group.update(
        db_obj=db_user_group,
        obj_in=item_in,
        projects=db_provider_with_multiple_projects.projects,
        force=True,
    )
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)
    assert len(item.slas) == 2


def test_add_new_sla_replacing_part_of_existing_one(
    db_user_group_with_sla_with_multiple_projects: UserGroup,
) -> None:
    """Update the attributes and relationships of an existing User Group.

    Update a User Group with an SLA pointing to multiple projects (each on a different
    provider), adding a new SLA pointing to a project of an already referenced provider.
    The user group will have 2 SLAs each pointing to the project of one provider.

    This case should happen when updating the SLA of a project and the old SLA, pointing
    to 2 providers, should be changed as well!
    """
    db_sla = db_user_group_with_sla_with_multiple_projects.slas.single()
    db_project = db_sla.projects.single()
    db_provider = db_project.provider.single()
    item_in = create_random_user_group(project=db_project.uuid)
    item = user_group.update(
        db_obj=db_user_group_with_sla_with_multiple_projects,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)
    assert len(item.slas) == 2
    db_sla1 = item.slas.all()[0]
    db_sla2 = item.slas.all()[1]
    assert len(db_sla1.projects) == 1
    assert len(db_sla2.projects) == 1
    db_project1 = db_sla1.projects.single()
    db_project2 = db_sla2.projects.single()
    assert db_project1.sla.single()
    assert db_project2.sla.single()
    assert db_project1.provider.single() != db_project2.provider.single()


def test_delete_item_with_relationships(
    db_user_group: UserGroup,
) -> None:
    """Delete an existing User Group.

    On cascade delete linked SLAs.
    """
    db_idp = db_user_group.identity_provider.single()
    db_sla = db_user_group.slas.single()
    assert user_group.remove(db_obj=db_user_group)
    assert not user_group.get(uid=db_user_group.uid)
    assert identity_provider.get(uid=db_idp.uid)
    assert not sla.get(uid=db_sla.uid)
