from typing import Generator
from uuid import uuid4

from app.project.crud import project
from app.quota.crud import network_quota
from app.quota.models import NetworkQuota
from app.service.crud import network_service
from app.service.models import NetworkService
from tests.utils.network_quota import (
    create_random_network_quota,
    create_random_network_quota_patch,
    validate_create_network_quota_attrs,
)


def test_create_item(db_network_serv: NetworkService) -> None:
    """Create a Network Quota belonging to a specific Network Service."""
    db_region = db_network_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_network_quota(project=db_project.uuid)
    item = network_quota.create(
        obj_in=item_in, service=db_network_serv, project=db_project
    )
    validate_create_network_quota_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_network_serv: NetworkService) -> None:
    """Create a Network Quota, with default values when possible, belonging to a
    specific Network Service.
    """
    db_region = db_network_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_network_quota(default=True, project=db_project.uuid)
    item = network_quota.create(
        obj_in=item_in, service=db_network_serv, project=db_project
    )
    validate_create_network_quota_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_network_quota: NetworkQuota) -> None:
    """Retrieve a Network Quota from its UID."""
    item = network_quota.get(uid=db_network_quota.uid)
    assert item.uid == db_network_quota.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing Network Quota."""
    assert not network_quota.get(uid=uuid4())


def test_get_items(
    db_network_quota: NetworkQuota, db_network_quota_per_user: NetworkQuota
) -> None:
    """Retrieve multiple Network Quotas."""
    stored_items = network_quota.get_multi()
    assert len(stored_items) == 2

    stored_items = network_quota.get_multi(uid=db_network_quota.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_network_quota.uid

    stored_items = network_quota.get_multi(uid=db_network_quota_per_user.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_network_quota_per_user.uid


def test_get_items_with_limit(
    db_network_quota: NetworkQuota, db_network_quota_per_user: NetworkQuota
) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = network_quota.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = network_quota.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = network_quota.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(
    db_network_quota: NetworkQuota, db_network_quota_per_user: NetworkQuota
) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = sorted(network_quota.get_multi(), key=lambda x: x.uid)

    stored_items = network_quota.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = network_quota.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(
    db_network_quota: NetworkQuota, db_network_quota_per_user: NetworkQuota
) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = network_quota.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = network_quota.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_network_quota: NetworkQuota) -> None:
    """Update the attributes of an existing Network Quota, do not update linked
    relationships.
    """
    patch_in = create_random_network_quota_patch()
    item = network_quota.update(db_obj=db_network_quota, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_network_quota: NetworkQuota) -> None:
    """Try to update the attributes of an existing Network Quota, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
    """
    patch_in = create_random_network_quota_patch(default=True)
    assert not network_quota.update(db_obj=db_network_quota, obj_in=patch_in)

    patch_in = create_random_network_quota_patch(default=True)
    patch_in.description = ""
    item = network_quota.update(db_obj=db_network_quota, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_network_quota.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_replace_project_with_another_same_provider(
    db_network_quota: NetworkQuota,
) -> None:
    """Update the attributes and relationships of an existing Network Quota.

    At first update a Network Quota with a set of linked projects, updating its
    attributes and removing all linked projects.
    """
    db_project = db_network_quota.project.single()
    db_provider = db_project.provider.single()
    for db_project2 in db_provider.projects:
        if db_project2.uid != db_project.uid:
            break
    item_in = create_random_network_quota(project=db_project2.uuid)
    item = network_quota.update(
        db_obj=db_network_quota,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_network_quota_attrs(obj_in=item_in, db_item=item)


def test_force_update_without_changing_relationships(
    db_network_quota: NetworkQuota,
) -> None:
    """Update the attributes and relationships of an existing Network Quota.

    Update a Network Quota with a set of linked projects, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_service = db_network_quota.service.single()
    db_project = db_network_quota.project.single()
    db_provider = db_project.provider.single()
    item_in = create_random_network_quota(project=db_project.uuid)
    item = network_quota.update(
        db_obj=db_network_quota,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_network_quota_attrs(obj_in=item_in, db_item=item)
    assert item.service.single() == db_service
    assert item.project.single() == db_project


def test_delete_item(db_network_quota: NetworkQuota) -> None:
    """Delete an existing Network Quota.

    Do not delete related projects.
    """
    db_project = db_network_quota.project.single()
    db_service = db_network_quota.service.single()
    assert network_quota.remove(db_obj=db_network_quota)
    assert not network_quota.get(uid=db_network_quota.uid)
    assert project.get(uid=db_project.uid)
    assert network_service.get(uid=db_service.uid)
