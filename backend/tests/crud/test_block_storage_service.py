from uuid import uuid4

from app.quota.crud import block_storage_quota
from app.region.models import Region
from app.service.crud import block_storage_service
from app.service.models import BlockStorageService
from tests.utils.block_storage_service import (
    create_random_block_storage_service,
    create_random_block_storage_service_patch,
    validate_create_block_storage_service_attrs,
)


def test_create_item(db_region: Region) -> None:
    """Create a BlockStorage Service belonging to a specific Region."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_region: Region) -> None:
    """Create a BlockStorage Service, with default values when possible,
    belonging to a specific Region."""
    item_in = create_random_block_storage_service(default=True)
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects(db_region: Region) -> None:
    """Create a BlockStorage Service belonging to a specific Region with a set
    of quotas."""
    db_provider = db_region.provider.single()
    item_in = create_random_block_storage_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = block_storage_service.create(
        obj_in=item_in, region=db_region, projects=db_provider.projects
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_block_storage_serv: BlockStorageService) -> None:
    """Retrieve a BlockStorage Service from its UID."""
    item = block_storage_service.get(uid=db_block_storage_serv.uid)
    assert item.uid == db_block_storage_serv.uid


def test_get_non_existing_item() -> None:
    """Try to retrieve a not existing BlockStorage Service."""
    assert not block_storage_service.get(uid=uuid4())


def test_get_items(
    db_block_storage_serv: BlockStorageService,
    db_block_storage_serv2: BlockStorageService,
) -> None:
    """Retrieve multiple BlockStorage Services."""
    stored_items = block_storage_service.get_multi()
    assert len(stored_items) == 2

    stored_items = block_storage_service.get_multi(uid=db_block_storage_serv.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_block_storage_serv.uid

    stored_items = block_storage_service.get_multi(uid=db_block_storage_serv2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_block_storage_serv2.uid


def test_get_items_with_limit(
    db_block_storage_serv: BlockStorageService,
    db_block_storage_serv2: BlockStorageService,
) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = block_storage_service.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = block_storage_service.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = block_storage_service.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(
    db_block_storage_serv: BlockStorageService,
    db_block_storage_serv2: BlockStorageService,
) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = list(sorted(block_storage_service.get_multi(), key=lambda x: x.uid))

    stored_items = block_storage_service.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = block_storage_service.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(
    db_block_storage_serv: BlockStorageService,
    db_block_storage_serv2: BlockStorageService,
) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = block_storage_service.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = block_storage_service.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_region: Region) -> None:
    """Update the attributes of an existing BlockStorage Service, without
    updating its relationships."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    patch_in = create_random_block_storage_service_patch()
    item = block_storage_service.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_region: Region) -> None:
    """Try to update the attributes of an existing BlockStorage Service,
    without updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    patch_in = create_random_block_storage_service_patch(default=True)
    assert not block_storage_service.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_block_storage_service_patch(default=True)
    patch_in.description = ""
    item = block_storage_service.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_(db_region: Region) -> None:
    """Update the attributes and relationships of an existing BlockStorage
    Service.

    At first update a BlockStorage Service with a set of linked
    projects, updating its attributes and removing all linked projects.

    Update a BlockStorage Service with no projects, changing its
    attributes and linking a new project.

    Update a BlockStorage Service with a set of linked projects,
    changing both its attributes and replacing the linked projects with
    new ones.

    Update a BlockStorage Service with a set of linked projects,
    changing only its attributes leaving untouched its connections (this
    is different from the previous test because the flag force is set to
    True).
    """
    db_provider = db_region.provider.single()
    item_in = create_random_block_storage_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = block_storage_service.create(
        obj_in=item_in, region=db_region, projects=db_provider.projects
    )
    item_in = create_random_block_storage_service()
    item = block_storage_service.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_block_storage_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = block_storage_service.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_block_storage_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = block_storage_service.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)

    quotas = item_in.quotas
    item_in = create_random_block_storage_service()
    item_in.quotas = quotas
    item = block_storage_service.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_region: Region) -> None:
    """Delete an existing BlockStorage Service."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    result = block_storage_service.remove(db_obj=item)
    assert result
    item = block_storage_service.get(uid=item.uid)
    assert not item
    assert db_region


def test_delete_item_with_relationships(db_region: Region) -> None:
    """Delete an existing BlockStorage Service and its linked quotas."""
    db_provider = db_region.provider.single()
    item_in = create_random_block_storage_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = block_storage_service.create(
        obj_in=item_in, region=db_region, projects=db_provider.projects
    )
    db_quota = item.quotas.single()

    result = block_storage_service.remove(db_obj=item)
    assert result
    item = block_storage_service.get(uid=item.uid)
    assert not item
    item = block_storage_quota.get(uid=db_quota.uid)
    assert not item
