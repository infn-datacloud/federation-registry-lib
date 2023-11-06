from typing import Generator
from uuid import uuid4

from app.project.crud import project
from app.project.models import Project
from app.provider.crud import provider
from app.provider.models import Provider
from app.quota.crud import block_storage_quota, compute_quota
from app.quota.models import ComputeQuota
from app.sla.crud import sla
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
    """Create a Project, with default values when possible, belonging to a specific
    Provider."""
    item_in = create_random_project(default=True)
    item = project.create(obj_in=item_in, provider=db_provider)
    validate_create_project_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_project: Project) -> None:
    """Retrieve a Project from its UID."""
    item = project.get(uid=db_project.uid)
    assert item.uid == db_project.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing Project."""
    assert not project.get(uid=uuid4())


def test_get_items(db_project: Project, db_project2: Project) -> None:
    """Retrieve multiple Projects."""
    stored_items = project.get_multi()
    assert len(stored_items) == 2

    stored_items = project.get_multi(uid=db_project.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_project.uid

    stored_items = project.get_multi(uid=db_project2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_project2.uid


def test_get_items_with_limit(db_project: Project, db_project2: Project) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = project.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = project.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = project.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_project: Project, db_project2: Project) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = list(sorted(project.get_multi(), key=lambda x: x.uid))

    stored_items = project.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = project.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_project: Project, db_project2: Project) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = project.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = project.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_project: Project) -> None:
    """Update the attributes of an existing Project, without updating its
    relationships."""
    patch_in = create_random_project_patch()
    item = project.update(db_obj=db_project, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_project: Project) -> None:
    """Try to update the attributes of an existing Project, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
    """
    patch_in = create_random_project_patch(default=True)
    assert not project.update(db_obj=db_project, obj_in=patch_in)

    patch_in = create_random_project_patch(default=True)
    patch_in.description = ""
    item = project.update(db_obj=db_project, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_project.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_force_update_without_changing_flavors(
    db_project_with_single_private_flavor: Project,
) -> None:
    """Update the attributes and relationships of an existing Project.

    Update a Project with a set of linked flavors, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_provider = db_project_with_single_private_flavor.provider.single()
    db_flavor = db_project_with_single_private_flavor.private_flavors.single()
    item_in = create_random_project()
    item = project.update(
        db_obj=db_project_with_single_private_flavor, obj_in=item_in, force=True
    )
    validate_create_project_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.private_flavors.single() == db_flavor


def test_force_update_without_changing_images(
    db_project_with_single_private_image: Project,
) -> None:
    """Update the attributes and relationships of an existing Project.

    Update a Project with a set of linked images, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_provider = db_project_with_single_private_image.provider.single()
    db_image = db_project_with_single_private_image.private_images.single()
    item_in = create_random_project()
    item = project.update(
        db_obj=db_project_with_single_private_image, obj_in=item_in, force=True
    )
    validate_create_project_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.private_images.single() == db_image


def test_force_update_without_changing_block_storage_quotas(
    db_project_with_single_block_storage_quota: Project,
) -> None:
    """Update the attributes and relationships of an existing Project.

    Update a Project with a set of linked quotas, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_provider = db_project_with_single_block_storage_quota.provider.single()
    db_quota = db_project_with_single_block_storage_quota.quotas.single()
    item_in = create_random_project()
    item = project.update(
        db_obj=db_project_with_single_block_storage_quota, obj_in=item_in, force=True
    )
    validate_create_project_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.quotas.single() == db_quota


def test_force_update_without_changing_compute_quotas(
    db_project_with_single_compute_quota: Project,
) -> None:
    """Update the attributes and relationships of an existing Project.

    Update a Project with a set of linked quotas, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_provider = db_project_with_single_compute_quota.provider.single()
    db_quota = db_project_with_single_compute_quota.quotas.single()
    item_in = create_random_project()
    item = project.update(
        db_obj=db_project_with_single_compute_quota, obj_in=item_in, force=True
    )
    validate_create_project_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.quotas.single() == db_quota


def test_force_update_without_changing_slas(
    db_project_with_sla: Project,
) -> None:
    """Update the attributes and relationships of an existing Project.

    Update a Project with a set of linked quotas, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_provider = db_project_with_sla.provider.single()
    db_quota = db_project_with_sla.quotas.single()
    item_in = create_random_project()
    item = project.update(db_obj=db_project_with_sla, obj_in=item_in, force=True)
    validate_create_project_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.quotas.single() == db_quota


# def test_force_update_item_with_defaults(db_provider: Provider) -> None:
#     """Update the attributes and relationships of an existing Location.

#     Update a Region with a set of linked locations, changing
#     only its attributes leaving untouched its connections (this is
#     different from the previous test because the flag force is set to
#     True).
#     """
#     item_in = create_random_project()
#     item = project.create(obj_in=item_in, provider=db_provider)
#     item_in = create_random_project(default=True)
#     item = project.update(db_obj=item, obj_in=item_in, force=True)
#     validate_create_project_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_project: Project) -> None:
    """Delete an existing Project."""
    db_provider = db_project.provider.single()
    assert project.remove(db_obj=db_project)
    assert not project.get(uid=db_project.uid)
    assert provider.get(uid=db_provider.uid)


def test_delete_item_with_proprietary_sla(db_project_with_sla: Project) -> None:
    """Delete an existing Project and its SLA."""
    db_provider = db_project_with_sla.provider.single()
    db_sla = db_project_with_sla.sla.single()
    assert project.remove(db_obj=db_project_with_sla)
    assert not project.get(uid=db_project_with_sla.uid)
    assert provider.get(uid=db_provider.uid)
    assert not sla.get(uid=db_sla.uid)


def test_delete_item_with_shared_sla(db_project_with_shared_sla: Project) -> None:
    """Delete an existing Project but not its SLA, since it is shared."""
    db_provider = db_project_with_shared_sla.provider.single()
    db_sla = db_project_with_shared_sla.sla.single()
    assert project.remove(db_obj=db_project_with_shared_sla)
    assert not project.get(uid=db_project_with_shared_sla.uid)
    assert provider.get(uid=db_provider.uid)
    assert sla.get(uid=db_sla.uid)


def test_delete_item_with_block_storage_quotas(
    db_project_with_single_block_storage_quota: Project,
) -> None:
    """Delete an existing Project and its BlockStorage Quotas."""
    db_provider = db_project_with_single_block_storage_quota.provider.single()
    db_quota = db_project_with_single_block_storage_quota.quotas.single()
    assert project.remove(db_obj=db_project_with_single_block_storage_quota)
    assert not project.get(uid=db_project_with_single_block_storage_quota.uid)
    assert provider.get(uid=db_provider.uid)
    assert not block_storage_quota.get(uid=db_quota.uid)


def test_delete_item_with_compute_quotas(
    db_project_with_single_compute_quota: ComputeQuota,
) -> None:
    """Delete an existing Project and its Compute Quotas."""
    db_provider = db_project_with_single_compute_quota.provider.single()
    db_quota = db_project_with_single_compute_quota.quotas.single()
    assert project.remove(db_obj=db_project_with_single_compute_quota)
    assert not project.get(uid=db_project_with_single_compute_quota.uid)
    assert provider.get(uid=db_provider.uid)
    assert not compute_quota.get(uid=db_quota.uid)
