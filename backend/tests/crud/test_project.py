from uuid import uuid4

from app.project.crud import project
from app.project.models import Project
from app.provider.models import Provider
from app.quota.crud import block_storage_quota, compute_quota
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.sla.crud import sla
from app.sla.models import SLA
from tests.utils.project import (
    create_random_project,
    create_random_project_patch,
    validate_create_project_attrs,
)


def test_create_item(db_provider: Provider) -> None:
    """Create a Project belonging to a specific Provider."""
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    validate_create_project_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_provider: Provider) -> None:
    """Create a Project, with default values when possible, belonging to a
    specific Provider."""
    item_in = create_random_project(default=True)
    item = project.create(obj_in=item_in, provider=db_provider)
    validate_create_project_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_project: Project) -> None:
    """Retrieve a Project from its UID."""
    item = project.get(uid=db_project.uid)
    assert item.uid == db_project.uid


def test_get_non_existing_item() -> None:
    """Try to retrieve a not existing Project."""
    assert not project.get(uid=uuid4())


def test_get_items(db_provider: Provider) -> None:
    """Retrieve multiple Projects."""
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_project()
    item2 = project.create(obj_in=item_in2, provider=db_provider)

    stored_items = project.get_multi()
    assert len(stored_items) == 2

    stored_items = project.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_create_project_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = project.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_create_project_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_provider: Provider) -> None:
    """Test the 'limit' attribute in GET operations."""
    item_in = create_random_project()
    project.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_project()
    project.create(obj_in=item_in2, provider=db_provider)

    stored_items = project.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = project.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = project.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_provider: Provider) -> None:
    """Test the 'sort' attribute in GET operations."""
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_project()
    item2 = project.create(obj_in=item_in2, provider=db_provider)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = project.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = project.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_provider: Provider) -> None:
    """Test the 'skip' attribute in GET operations."""
    item_in = create_random_project()
    project.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_project()
    project.create(obj_in=item_in2, provider=db_provider)

    stored_items = project.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = project.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_provider: Provider) -> None:
    """Update the attributes of an existing Project, without updating its
    relationships."""
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    patch_in = create_random_project_patch()
    item = project.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_project_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_provider: Provider) -> None:
    """Try to update the attributes of an existing Project, without updating
    its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    patch_in = create_random_project_patch(default=True)
    assert not project.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_project_patch(default=True)
    patch_in.description = ""
    item = project.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_project_attrs(obj_in=item_in, db_item=item)


def test_force_update_item(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_project()
    item = project.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_project_attrs(obj_in=item_in, db_item=item)


def test_force_update_item_with_defaults(db_provider: Provider) -> None:
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_project(default=True)
    item = project.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_project_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_provider: Provider) -> None:
    """Delete an existing Project."""
    item_in = create_random_project()
    item = project.create(obj_in=item_in, provider=db_provider)
    result = project.remove(db_obj=item)
    assert result
    item = project.get(uid=item.uid)
    assert not item
    assert db_provider


def test_delete_item_with_proprietary_sla(db_sla: SLA) -> None:
    """Delete an existing Project and its SLA."""
    item = db_sla.projects.single()
    result = project.remove(db_obj=item)
    assert result
    item = project.get(uid=item.uid)
    assert not item
    item = sla.get(uid=db_sla.uid)
    assert not item


# TODO tests deletion of project linked to a SLA related to multiple projects.
# The deletion delete the project but not the SLA.


def test_delete_item_with_block_storage_quotas(
    db_block_storage_quota: BlockStorageQuota,
) -> None:
    """Delete an existing Project and its BlockStorage Quotas."""
    item = db_block_storage_quota.project.single()
    result = project.remove(db_obj=item)
    assert result
    item = project.get(uid=item.uid)
    assert not item
    item = block_storage_quota.get(uid=db_block_storage_quota.uid)
    assert not item


def test_delete_item_with_compute_quotas(db_compute_quota: ComputeQuota) -> None:
    """Delete an existing Project and its Compute Quotas."""
    item = db_compute_quota.project.single()
    result = project.remove(db_obj=item)
    assert result
    item = project.get(uid=item.uid)
    assert not item
    item = compute_quota.get(uid=db_compute_quota.uid)
    assert not item
