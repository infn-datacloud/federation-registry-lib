from uuid import uuid4

from app.project.crud import project
from app.quota.crud import compute_quota
from app.quota.models import ComputeQuota
from app.service.models import ComputeService
from tests.utils.compute_quota import (
    create_random_compute_quota,
    create_random_compute_quota_patch,
    validate_create_compute_quota_attrs,
)
from tests.utils.project import create_random_project


def test_create_item(db_compute_serv: ComputeService) -> None:
    """Create a Compute Quota belonging to a specific Compute Service."""
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    validate_create_compute_quota_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_compute_serv: ComputeService) -> None:
    """Create a Compute Quota, with default values when possible, belonging to
    a specific Compute Service."""
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(default=True, project=db_project.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    validate_create_compute_quota_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_compute_quota: ComputeQuota) -> None:
    """Retrieve a Compute Quota from its UID."""
    item = compute_quota.get(uid=db_compute_quota.uid)
    assert item.uid == db_compute_quota.uid


def test_get_non_existing_item() -> None:
    """Try to retrieve a not existing Compute Quota."""
    assert not compute_quota.get(uid=uuid4())


def test_get_items(db_compute_serv: ComputeService) -> None:
    """Retrieve multiple Compute Quotas."""
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    item_in2 = create_random_compute_quota(project=db_project.uuid)
    item2 = compute_quota.create(
        obj_in=item_in2, service=db_compute_serv, project=db_project
    )

    stored_items = compute_quota.get_multi()
    assert len(stored_items) == 2

    stored_items = compute_quota.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_create_compute_quota_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = compute_quota.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_create_compute_quota_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_compute_serv: ComputeService) -> None:
    """Test the 'limit' attribute in GET operations."""
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    compute_quota.create(obj_in=item_in, service=db_compute_serv, project=db_project)
    item_in2 = create_random_compute_quota(project=db_project.uuid)
    compute_quota.create(obj_in=item_in2, service=db_compute_serv, project=db_project)

    stored_items = compute_quota.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = compute_quota.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = compute_quota.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_compute_serv: ComputeService) -> None:
    """Test the 'sort' attribute in GET operations."""
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    item_in2 = create_random_compute_quota(project=db_project.uuid)
    item2 = compute_quota.create(
        obj_in=item_in2, service=db_compute_serv, project=db_project
    )

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = compute_quota.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = compute_quota.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_compute_serv: ComputeService) -> None:
    """Test the 'skip' attribute in GET operations."""
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    compute_quota.create(obj_in=item_in, service=db_compute_serv, project=db_project)
    item_in2 = create_random_compute_quota(project=db_project.uuid)
    compute_quota.create(obj_in=item_in2, service=db_compute_serv, project=db_project)

    stored_items = compute_quota.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = compute_quota.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_compute_serv: ComputeService) -> None:
    """Update the attributes of an existing Compute Quota, do not update linked
    relationships."""
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    patch_in = create_random_compute_quota_patch()
    item = compute_quota.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_compute_quota_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_compute_serv: ComputeService) -> None:
    """Try to update the attributes of an existing Compute Quota, without
    updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    patch_in = create_random_compute_quota_patch(default=True)
    assert not compute_quota.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_compute_quota_patch(default=True)
    patch_in.description = ""
    item = compute_quota.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_compute_quota_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item(db_compute_serv: ComputeService) -> None:
    """Update the attributes and relationships of an existing Compute Quota.

    At first update a Compute Quota with a set of linked projects,
    updating its attributes and removing all linked projects.

    Update a Compute Quota with a set of linked projects, changing only
    its attributes leaving untouched its connections (this is different
    from the previous test because the flag force is set to True).
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    project1 = db_provider.projects.single()
    item_in = create_random_compute_quota(project=project1.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=project1
    )

    project2 = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_compute_quota(project=project2.uuid)
    item = compute_quota.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_compute_quota_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_compute_quota(project=item_in.project)
    item = compute_quota.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_compute_quota_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_compute_serv: ComputeService) -> None:
    """Delete an existing Compute Quota.

    Do not delete related projects.
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    num_db_project = len(db_provider.projects)
    result = compute_quota.remove(db_obj=item)
    assert result
    item = compute_quota.get(uid=item.uid)
    assert not item
    assert len(db_provider.projects) == num_db_project
