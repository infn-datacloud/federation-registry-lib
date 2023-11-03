from copy import deepcopy
from typing import Generator
from uuid import uuid4

from app.quota.crud import block_storage_quota
from app.region.crud import region
from app.region.models import Region
from app.service.crud import block_storage_service
from app.service.models import BlockStorageService
from tests.utils.block_storage_service import (
    create_random_block_storage_service,
    create_random_block_storage_service_patch,
    validate_create_block_storage_service_attrs,
)
from tests.utils.utils import random_lower_string


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


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
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


def test_patch_item(db_block_storage_serv: BlockStorageService) -> None:
    """Update the attributes of an existing BlockStorage Service, without
    updating its relationships."""
    patch_in = create_random_block_storage_service_patch()
    item = block_storage_service.update(db_obj=db_block_storage_serv, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_block_storage_serv: BlockStorageService) -> None:
    """Try to update the attributes of an existing BlockStorage Service,
    without updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    patch_in = create_random_block_storage_service_patch(default=True)
    assert not block_storage_service.update(
        db_obj=db_block_storage_serv, obj_in=patch_in
    )

    patch_in = create_random_block_storage_service_patch(default=True)
    patch_in.description = ""
    item = block_storage_service.update(db_obj=db_block_storage_serv, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_block_storage_serv.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_add_quotas(db_block_storage_serv: BlockStorageService) -> None:
    """Update the attributes and relationships of an existing BlockStorage
    Service.

    Update a BlockStorage Service with no quotas, changing its
    attributes and linking a new quota.
    """
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_block_storage_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    db_quota = deepcopy(item_in.quotas[0])
    db_quota.description = random_lower_string()
    db_quota.per_user = not db_quota.per_user
    item_in.quotas.append(db_quota)

    item = block_storage_service.update(
        db_obj=db_block_storage_serv,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.quotas) == 2


def test_remove_quotas(
    db_block_storage_serv_with_multiple_quotas: BlockStorageService,
) -> None:
    """Update the attributes and relationships of an existing BlockStorage
    Service.

    Update a BlockStorage Service with a set of linked quotas, updating
    its attributes and removing all linked quotas.
    """
    db_region = db_block_storage_serv_with_multiple_quotas.region.single()
    item_in = create_random_block_storage_service()
    item = block_storage_service.update(
        db_obj=db_block_storage_serv_with_multiple_quotas, obj_in=item_in, force=True
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.quotas) == 0


def test_replace_quotas_with_ones_pointing_to_diff_project(
    db_block_storage_serv_with_multiple_quotas_same_project: BlockStorageService,
) -> None:
    """Update the attributes and relationships of an existing BlockStorage
    Service.

    Update a BlockStorage Service with a set of linked quotas, changing
    both its attributes and replacing the linked quotas with new ones.
    """
    db_region = db_block_storage_serv_with_multiple_quotas_same_project.region.single()
    db_provider = db_region.provider.single()
    db_quota = db_block_storage_serv_with_multiple_quotas_same_project.quotas.get(
        per_user=True
    )
    for db_project in db_provider.projects:
        if db_project.uid != db_quota.project.single().uid:
            break

    quotas_uids = [
        i.uid for i in db_block_storage_serv_with_multiple_quotas_same_project.quotas
    ]

    item_in = create_random_block_storage_service(projects=[db_project.uuid])
    db_quota = deepcopy(item_in.quotas[0])
    db_quota.description = random_lower_string()
    db_quota.per_user = not db_quota.per_user
    item_in.quotas.append(db_quota)

    item = block_storage_service.update(
        db_obj=db_block_storage_serv_with_multiple_quotas_same_project,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.quotas) == 2
    for i in item.quotas:
        assert i.uid not in quotas_uids


def test_replace_quotas_with_ones_pointing_to_same_project(
    db_block_storage_serv_with_multiple_quotas_same_project: BlockStorageService,
) -> None:
    """Update the attributes and relationships of an existing BlockStorage
    Service.

    Update a BlockStorage Service with a set of linked quotas, changing
    both its attributes and replacing the linked quotas with new ones.
    """
    db_region = db_block_storage_serv_with_multiple_quotas_same_project.region.single()
    db_provider = db_region.provider.single()
    db_quota = db_block_storage_serv_with_multiple_quotas_same_project.quotas.get(
        per_user=True
    )
    db_project = db_quota.project.single()

    quotas_uids = [
        i.uid for i in db_block_storage_serv_with_multiple_quotas_same_project.quotas
    ]

    item_in = create_random_block_storage_service(projects=[db_project.uuid])
    db_quota = deepcopy(item_in.quotas[0])
    db_quota.description = random_lower_string()
    db_quota.per_user = not db_quota.per_user
    item_in.quotas.append(db_quota)

    item = block_storage_service.update(
        db_obj=db_block_storage_serv_with_multiple_quotas_same_project,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.quotas) == 2
    for i in sorted(item.quotas, key=lambda x: x.uid):
        assert i.uid in quotas_uids


def test_force_update_without_changing_relationships(
    db_block_storage_serv_with_single_quota: BlockStorageService,
) -> None:
    """Update the attributes and relationships of an existing BlockStorage
    Service.

    Update a BlockStorage Service with a set of linked quotas, changing
    only its attributes leaving untouched its connections (this is
    different from the previous test because the flag force is set to
    True).
    """
    db_region = db_block_storage_serv_with_single_quota.region.single()
    db_provider = db_region.provider.single()
    db_quota = db_block_storage_serv_with_single_quota.quotas.single()
    item_in = create_random_block_storage_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    for k in item_in.quotas[0].dict(exclude={"project"}).keys():
        item_in.quotas[0].__setattr__(k, db_quota.__getattribute__(k))
    item_in.quotas[0].project = db_quota.project.single().uuid
    item = block_storage_service.update(
        db_obj=db_block_storage_serv_with_single_quota,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_block_storage_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert item.quotas.single() == db_quota


def test_delete_item(db_block_storage_serv: BlockStorageService) -> None:
    """Delete an existing BlockStorage Service."""
    db_region = db_block_storage_serv.region.single()
    assert block_storage_service.remove(db_obj=db_block_storage_serv)
    assert not block_storage_service.get(uid=db_block_storage_serv.uid)
    assert region.get_multi(uid=db_region.uid)


def test_delete_item_with_relationships(
    db_block_storage_serv_with_single_quota: BlockStorageService,
) -> None:
    """Delete an existing BlockStorage Service and its linked quotas."""
    db_region = db_block_storage_serv_with_single_quota.region.single()
    db_quota = db_block_storage_serv_with_single_quota.quotas.single()
    assert block_storage_service.remove(db_obj=db_block_storage_serv_with_single_quota)
    assert not block_storage_service.get(
        uid=db_block_storage_serv_with_single_quota.uid
    )
    assert region.get(uid=db_region.uid)
    assert not block_storage_quota.get(uid=db_quota.uid)
