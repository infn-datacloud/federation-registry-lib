from typing import Generator
from uuid import uuid4

from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.project.crud import project
from app.service.crud import compute_service
from app.service.models import ComputeService
from tests.utils.flavor import (
    create_random_flavor,
    create_random_flavor_patch,
    validate_create_flavor_attrs,
)


def test_create_item(db_compute_serv: ComputeService) -> None:
    """Create a public Flavor belonging to a specific Compute Service."""
    item_in = create_random_flavor()
    item = flavor.create(obj_in=item_in, service=db_compute_serv)
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_compute_serv: ComputeService) -> None:
    """Create a public Flavor, with default values when possible, belonging to a
    specific Compute Service.
    """
    item_in = create_random_flavor(default=True)
    item = flavor.create(obj_in=item_in, service=db_compute_serv)
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)


def test_create_item_private(db_compute_serv: ComputeService) -> None:
    """Create a private Flavor belonging to a specific Compute Service.

    Private Flavors requires a list of allowed projects.
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
    item = flavor.create(
        obj_in=item_in, service=db_compute_serv, projects=db_provider.projects
    )
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_same_uuid_diff_provider(
    db_compute_serv: ComputeService, db_compute_serv2: ComputeService
) -> None:
    """Create a public Flavor belonging to a specific Compute Service.

    Connect a Flavor with the same UUID to another Provider. This operation is allowed
    since the flavors belong to different providers.
    """
    item_in = create_random_flavor()
    item = flavor.create(obj_in=item_in, service=db_compute_serv)
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    item2 = flavor.create(obj_in=item_in, service=db_compute_serv2)
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    assert item.uid != item2.uid


def test_connect_same_item_to_different_service(
    db_compute_serv2: ComputeService, db_compute_serv3: ComputeService
) -> None:
    """Create a public Flavor belonging to a specific Compute Service.

    Connect this same Flavor to another Compute Service of the same Provider. This
    operation is performed creating again the same flavor but passing another service.
    """
    item_in = create_random_flavor()
    item = flavor.create(obj_in=item_in, service=db_compute_serv2)
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    item2 = flavor.create(obj_in=item_in, service=db_compute_serv3)
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    assert item.uid == item2.uid


def test_get_item(db_private_flavor: Flavor) -> None:
    """Retrieve a Flavor from its UID."""
    item = flavor.get(uid=db_private_flavor.uid)
    assert item.uid == db_private_flavor.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing Flavor."""
    assert not flavor.get(uid=uuid4())


def test_get_items(db_public_flavor: Flavor, db_private_flavor: Flavor) -> None:
    """Retrieve multiple Flavors."""
    stored_items = flavor.get_multi()
    assert len(stored_items) == 2

    stored_items = flavor.get_multi(uid=db_public_flavor.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_public_flavor.uid

    stored_items = flavor.get_multi(uid=db_private_flavor.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_private_flavor.uid


def test_get_items_with_limit(
    db_public_flavor: Flavor, db_private_flavor: Flavor
) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = flavor.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = flavor.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = flavor.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_public_flavor: Flavor, db_private_flavor: Flavor) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = sorted(flavor.get_multi(), key=lambda x: x.uid)

    stored_items = flavor.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = flavor.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(
    db_public_flavor: Flavor, db_private_flavor: Flavor
) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = flavor.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = flavor.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_private_flavor: Flavor) -> None:
    """Update the attributes of an existing Flavor, without updating its
    relationships.
    """
    patch_in = create_random_flavor_patch()
    patch_in.is_public = db_private_flavor.is_public
    item = flavor.update(db_obj=db_private_flavor, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_private_flavor: Flavor) -> None:
    """Try to update the attributes of an existing Flavor, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
    """
    patch_in = create_random_flavor_patch(default=True)
    assert not flavor.update(db_obj=db_private_flavor, obj_in=patch_in)

    patch_in = create_random_flavor_patch(default=True)
    patch_in.description = ""
    patch_in.is_public = db_private_flavor.is_public
    item = flavor.update(db_obj=db_private_flavor, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_private_flavor.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


# TODO try to patch flavor setting it as private when there are no projects
# or public when it has related projects


def test_change_flavor_from_private_to_public(db_private_flavor: Flavor) -> None:
    """Update the attributes and relationships of an existing Flavor.

    Update a Flavor with a set of linked projects, updating its attributes and removing
    all linked projects. Change it from private to public.
    """
    item_in = create_random_flavor()
    item = flavor.update(db_obj=db_private_flavor, obj_in=item_in, force=True)
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)


def test_change_flavor_from_public_to_private(db_public_flavor: Flavor) -> None:
    """Update the attributes and relationships of an existing Flavor.

    Update a Flavor with no projects, changing its attributes and linking a new project.
    Change it from public to private.
    """
    db_service = db_public_flavor.services.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
    item = flavor.update(
        db_obj=db_public_flavor,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)


def test_replace_private_flavor_projects(db_private_flavor: Flavor) -> None:
    """Update the attributes and relationships of an existing Flavor.

    Update a Flavor with a set of linked projects, changing both its attributes and
    replacing the linked projects with new ones.
    """
    db_project = db_private_flavor.projects.single()
    db_provider = db_project.provider.single()
    item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
    item = flavor.update(
        db_obj=db_private_flavor,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)


def test_force_update_without_changing_relationships(db_private_flavor: Flavor) -> None:
    """Update the attributes and relationships of an existing Flavor.

    Update a Flavor with a set of linked projects, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_projects = sorted(db_private_flavor.projects, key=lambda x: x.uid)
    db_services = sorted(db_private_flavor.services, key=lambda x: x.uid)
    item_in = create_random_flavor(
        projects=[i.uuid for i in db_private_flavor.projects]
    )
    item = flavor.update(db_obj=db_private_flavor, obj_in=item_in, force=True)
    validate_create_flavor_attrs(obj_in=item_in, db_item=item)
    for i, j in zip(sorted(item.projects, key=lambda x: x.uid), db_projects):
        assert i == j
    for i, j in zip(sorted(item.services, key=lambda x: x.uid), db_services):
        assert i == j


def test_delete_item(db_public_flavor: Flavor) -> None:
    """Delete an existing public Flavor."""
    db_service = db_public_flavor.services.single()
    assert flavor.remove(db_obj=db_public_flavor)
    assert not flavor.get(uid=db_public_flavor.uid)
    assert compute_service.get(uid=db_service.uid)


def test_delete_item_with_relationships(db_private_flavor: Flavor) -> None:
    """Delete an existing private Flavor.

    Do not delete linked projects
    """
    db_service = db_private_flavor.services.single()
    db_project = db_private_flavor.projects.single()
    assert flavor.remove(db_obj=db_private_flavor)
    assert not flavor.get(uid=db_private_flavor.uid)
    assert project.get(uid=db_project.uid)
    assert compute_service.get(uid=db_service.uid)
