from uuid import uuid4

from app.sla.crud import sla
from app.project.crud import project
from app.user_group.crud import user_group
from app.sla.models import SLA
from app.user_group.models import UserGroup
from scripts.models.provider import Provider
from tests.utils.sla import (
    create_random_sla,
    create_random_sla_patch,
    validate_create_sla_attrs,
)


def test_create_item(db_user_group: UserGroup) -> None:
    """Create an SLA belonging to a specific user group and pointing to an
    existing projects."""
    db_idp = db_user_group.identity_provider.single()
    db_provider = db_idp.providers.single()
    db_project = db_provider.projects.single()
    item_in = create_random_sla(project=db_project.uuid)
    item = sla.create(obj_in=item_in, user_group=db_user_group, project=db_project)
    validate_create_sla_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_user_group: UserGroup) -> None:
    """Create an SLA, with default values when possible, belonging to a
    specific user group and pointing to existing projects."""
    db_idp = db_user_group.identity_provider.single()
    db_provider = db_idp.providers.single()
    db_project = db_provider.projects.single()
    item_in = create_random_sla(default=True, project=db_project.uuid)
    item = sla.create(obj_in=item_in, user_group=db_user_group, project=db_project)
    validate_create_sla_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_sla: SLA) -> None:
    """Retrieve an SLA from its UID."""
    item = sla.get(uid=db_sla.uid)
    assert item.uid == db_sla.uid


def test_get_non_existing_item() -> None:
    """Try to retrieve a not existing SLA."""
    assert not sla.get(uid=uuid4())


def test_get_items(db_sla2: SLA, db_sla3: SLA) -> None:
    """Retrieve multiple SLAs."""
    stored_items = sla.get_multi()
    assert len(stored_items) == 2

    stored_items = sla.get_multi(uid=db_sla2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_sla2.uid

    stored_items = sla.get_multi(uid=db_sla3.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_sla3.uid


def test_get_items_with_limit(db_sla2: SLA, db_sla3: SLA) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = sla.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = sla.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = sla.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_sla2: SLA, db_sla3: SLA) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = list(sorted(sla.get_multi(), key=lambda x: x.uid))

    stored_items = sla.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = sla.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_sla2: SLA, db_sla3: SLA) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = sla.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = sla.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_user_group: UserGroup) -> None:
    """Update the attributes of an existing SLA, without updating its
    relationships."""
    db_idp = db_user_group.identity_provider.single()
    db_provider = db_idp.providers.all()[0]
    db_project = db_provider.projects.all()[0]
    item_in = create_random_sla(project=db_project.uuid)
    item = sla.create(obj_in=item_in, user_group=db_user_group, project=db_project)
    patch_in = create_random_sla_patch()
    item = sla.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_sla_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_user_group: UserGroup) -> None:
    """Try to update the attributes of an existing SLA, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    db_idp = db_user_group.identity_provider.single()
    db_provider = db_idp.providers.all()[0]
    db_project = db_provider.projects.all()[0]
    item_in = create_random_sla(project=db_project.uuid)
    item = sla.create(obj_in=item_in, user_group=db_user_group, project=db_project)
    patch_in = create_random_sla_patch(default=True)
    assert not sla.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_sla_patch(default=True)
    patch_in.description = ""
    item = sla.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_sla_attrs(obj_in=item_in, db_item=item)


def test_forced_update(db_user_group: UserGroup) -> None:
    """Update the attributes and relationships of an existing SLA.

    At first update only SLA attributes leaving untouched its
    connections (this is different from the previous test because the
    flag force is set to True).

    Then update the linked projects. The new project list will replace
    the previous linked projects.
    """
    db_idp = db_user_group.identity_provider.single()
    db_provider = db_idp.providers.all()[0]
    db_project = db_provider.projects.all()[0]
    item_in = create_random_sla(project=db_project.uuid)
    item = sla.create(obj_in=item_in, user_group=db_user_group, project=db_project)
    item_in = create_random_sla(project=db_project.uuid)
    item = sla.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_sla_attrs(obj_in=item_in, db_item=item)

    db_project = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_sla(project=db_project.uuid)
    item = sla.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_sla_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_sla: SLA) -> None:
    """Delete an existing SLA."""
    db_project = db_sla.projects.single()
    db_user_group = db_sla.user_group.single()
    assert sla.remove(db_obj=db_sla)
    assert not sla.get(uid=db_sla.uid)
    assert project.get(uid=db_project.uid)
    assert user_group.get(uid=db_user_group.uid)
