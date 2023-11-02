from uuid import uuid4

from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.project.crud import project
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
    """Create a User Group belonging to a specific Identity Provider with an
    SLA for each received project."""
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
    """Create a User Group, with default values when possible, belonging to a
    specific Identity Provider with an SLA for each received project."""
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


def test_get_non_existing_item() -> None:
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
    sorted_items = list(sorted(user_group.get_multi(), key=lambda x: x.uid))

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


def test_patch_item(db_idp_with_single_user_group: IdentityProvider) -> None:
    """Update the attributes of an existing User Group, without updating its
    relationships."""
    db_provider = db_idp_with_single_user_group.providers.single()
    db_project = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_user_group(project=db_project.uuid)
    item = user_group.create(
        obj_in=item_in,
        identity_provider=db_idp_with_single_user_group,
        projects=db_provider.projects,
    )
    patch_in = create_random_user_group_patch()
    item = user_group.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
    """Try to update the attributes of an existing User Group, without updating
    its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    db_provider = db_idp_with_single_user_group.providers.single()
    db_project = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_user_group(project=db_project.uuid)
    item = user_group.create(
        obj_in=item_in,
        identity_provider=db_idp_with_single_user_group,
        projects=db_provider.projects,
    )
    patch_in = create_random_user_group_patch(default=True)
    assert not user_group.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_user_group_patch(default=True)
    patch_in.description = ""
    item = user_group.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_slas(
    db_idp_with_single_user_group: IdentityProvider,
) -> None:
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
    db_provider = db_idp_with_single_user_group.providers.single()
    db_project = db_provider.projects.single()
    item_in = create_random_user_group(project=db_project.uuid)
    item = user_group.create(
        obj_in=item_in, identity_provider=db_idp_with_single_user_group
    )

    item_in = create_random_user_group(project=db_project.uuid)
    item = user_group.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)

    sla = item_in.sla
    item_in = create_random_user_group(project=db_project.uuid)
    item_in.sla = sla
    item = user_group.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_user_group_attrs(obj_in=item_in, db_item=item)


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
