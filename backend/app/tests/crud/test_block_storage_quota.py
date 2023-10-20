from uuid import uuid4

from app.project.crud import project
from app.quota.crud import block_storage_quota
from app.service.models import BlockStorageService
from app.tests.utils.project import create_random_project
from app.tests.utils.quota import (
    create_random_block_storage_quota,
    create_random_block_storage_quota_patch,
    validate_block_storage_quota_attrs,
)


def test_create_item(db_block_storage_serv: BlockStorageService) -> None:
    """Create a BlockStorage Quota belonging to a specific BlockStorage
    Service."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    validate_block_storage_quota_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_block_storage_serv: BlockStorageService) -> None:
    """Create a BlockStorage Quota, with default values when possible,
    belonging to a specific BlockStorage Service."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(default=True, project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    validate_block_storage_quota_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_block_storage_serv: BlockStorageService) -> None:
    """Retrieve a BlockStorage Quota from its UID."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    item = block_storage_quota.get(uid=item.uid)
    validate_block_storage_quota_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_block_storage_serv: BlockStorageService) -> None:
    """Try to retrieve a not existing BlockStorage Quota."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    item = block_storage_quota.get(uid=uuid4())
    assert not item


def test_get_items(db_block_storage_serv: BlockStorageService) -> None:
    """Retrieve multiple BlockStorage Quotas."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    item_in2 = create_random_block_storage_quota(project=db_project.uuid)
    item2 = block_storage_quota.create(
        obj_in=item_in2, service=db_block_storage_serv, project=db_project
    )

    stored_items = block_storage_quota.get_multi()
    assert len(stored_items) == 2

    stored_items = block_storage_quota.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_block_storage_quota_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = block_storage_quota.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_block_storage_quota_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_block_storage_serv: BlockStorageService) -> None:
    """Test the 'limit' attribute in GET operations."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    item_in2 = create_random_block_storage_quota(project=db_project.uuid)
    block_storage_quota.create(
        obj_in=item_in2, service=db_block_storage_serv, project=db_project
    )

    stored_items = block_storage_quota.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = block_storage_quota.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = block_storage_quota.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_block_storage_serv: BlockStorageService) -> None:
    """Test the 'sort' attribute in GET operations."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    item_in2 = create_random_block_storage_quota(project=db_project.uuid)
    item2 = block_storage_quota.create(
        obj_in=item_in2, service=db_block_storage_serv, project=db_project
    )

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = block_storage_quota.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = block_storage_quota.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_block_storage_serv: BlockStorageService) -> None:
    """Test the 'skip' attribute in GET operations."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    item_in2 = create_random_block_storage_quota(project=db_project.uuid)
    block_storage_quota.create(
        obj_in=item_in2, service=db_block_storage_serv, project=db_project
    )

    stored_items = block_storage_quota.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = block_storage_quota.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_block_storage_serv: BlockStorageService) -> None:
    """Update the attributes of an existing BlockStorage Quota, do not update
    linked relationships."""
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    patch_in = create_random_block_storage_quota_patch()
    item = block_storage_quota.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_block_storage_quota_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_block_storage_serv: BlockStorageService) -> None:
    """Try to update the attributes of an existing BlockStorage Quota, without
    updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    patch_in = create_random_block_storage_quota_patch(default=True)
    assert not block_storage_quota.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_block_storage_quota_patch(default=True)
    patch_in.description = ""
    item = block_storage_quota.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_block_storage_quota_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item(db_block_storage_serv: BlockStorageService) -> None:
    """Update the attributes and relationships of an existing BlockStorage
    Quota.

    At first update a BlockStorage Quota with a set of linked projects,
    updating its attributes and removing all linked projects.

    Update a BlockStorage Quota with a set of linked projects, changing
    only its attributes leaving untouched its connections (this is
    different from the previous test because the flag force is set to
    True).
    """
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    project1 = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=project1.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=project1
    )

    project2 = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_block_storage_quota(project=project2.uuid)
    item = block_storage_quota.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_block_storage_quota_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_block_storage_quota(project=item_in.project)
    item = block_storage_quota.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_block_storage_quota_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_block_storage_serv: BlockStorageService) -> None:
    """Delete an existing BlockStorage Quota.

    Do not delete related projects.
    """
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    num_db_project = len(db_provider.projects)
    result = block_storage_quota.remove(db_obj=item)
    assert result
    item = block_storage_quota.get(uid=item.uid)
    assert not item
    assert len(db_provider.projects) == num_db_project
