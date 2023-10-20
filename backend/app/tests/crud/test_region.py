from uuid import uuid4

from app.location.crud import location
from app.location.models import Location
from app.project.crud import project
from app.provider.models import Provider
from app.region.crud import region
from app.service.crud import (
    block_storage_service,
    compute_service,
    identity_service,
    network_service,
)
from app.service.enum import ServiceType
from app.tests.utils.project import create_random_project
from app.tests.utils.region import create_random_region, validate_region_attrs


def test_create_item(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_provider: Provider) -> None:
    """Create a Region, with default values when possible, belonging to a
    specific Provider."""
    item_in = create_random_region(default=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_location(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with a Location."""
    item_in = create_random_region(with_location=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_already_existing_location(db_location: Location) -> None:
    """Create a Region belonging to a specific Provider with an already
    existing Location.

    At first the new region points to a location with same site name but
    different attributes.

    In the latter the new location equals the existing one.

    Verify that no new locations have been created but all regions point
    to the same.
    """
    db_region = db_location.regions.all()[0]
    db_provider = db_region.provider.single()

    item_in = create_random_region(with_location=True)
    item_in.location.site = db_location.site
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)

    loc_in = item_in.location
    item_in = create_random_region()
    item_in.location = loc_in
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)

    assert len(location.get_multi()) == 1


def test_create_item_with_projects_and_block_storage_services(
    db_provider: Provider,
) -> None:
    """Create a Region belonging to a specific Provider with BlockStorage
    Services.

    On Cascade create related quotas
    """
    item_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_compute_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Compute Services.

    On Cascade create related quotas
    """
    item_in = create_random_region(
        with_compute_services=True, projects=[i.uuid for i in db_provider.projects]
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_identity_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Identity
    Services."""
    item_in = create_random_region(with_identity_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_network_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Network
    Services."""
    item_in = create_random_region(
        with_network_services=True, projects=[i.uuid for i in db_provider.projects]
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_everything(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Location,
    BlockStorage Services, Compute Services, Identity Services and Network
    Services."""
    item_in = create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_block_storage_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with BlockStorage
    Services.

    No quotas
    """
    item_in = create_random_region(with_block_storage_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_compute_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Compute Services.

    No quotas
    """
    item_in = create_random_region(with_compute_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_network_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Compute Services.

    Only public networks
    """
    item_in = create_random_region(with_network_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_provider: Provider) -> None:
    """Retrieve a Region from its UID."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    item = region.get(uid=item.uid)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_provider: Provider) -> None:
    """Try to retrieve a not existing Region."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    item = region.get(uid=uuid4())
    assert not item


def test_get_items(db_provider: Provider) -> None:
    """Retrieve multiple Regions."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_region()
    item2 = region.create(obj_in=item_in2, provider=db_provider)

    stored_items = region.get_multi()
    assert len(stored_items) == 2

    stored_items = region.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_region_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = region.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_region_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_provider: Provider) -> None:
    """Test the 'limit' attribute in GET operations."""
    item_in = create_random_region()
    region.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_region()
    region.create(obj_in=item_in2, provider=db_provider)

    stored_items = region.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = region.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = region.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_provider: Provider) -> None:
    """Test the 'sort' attribute in GET operations."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_region()
    item2 = region.create(obj_in=item_in2, provider=db_provider)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = region.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = region.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_provider: Provider) -> None:
    """Test the 'skip' attribute in GET operations."""
    item_in = create_random_region()
    region.create(obj_in=item_in, provider=db_provider)
    item_in2 = create_random_region()
    region.create(obj_in=item_in2, provider=db_provider)

    stored_items = region.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = region.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_provider: Provider) -> None:
    """Update the attributes of an existing Region, without updating its
    relationships."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_location(db_provider: Provider) -> None:
    """Update the attributes and relationships of an existing Region.

    At first update a Region with a location, updating its attributes
    and removing the location.

    Update a Region with no location, changing its attributes and
    linking a new location.

    Update a Region with a location, changing both its attributes and
    replacing the location with a new one.

    Update a Region with a location, changing only its attributes
    leaving untouched its connections (this is different from the
    previous test because the flag force is set to True).
    """
    item_in = create_random_region(with_location=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(with_location=True)
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(with_location=True)
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    loc_in = item_in.location
    item_in = create_random_region()
    item_in.location = loc_in
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_block_storage_services(
    db_provider: Provider,
) -> None:
    """Update the attributes and relationships of an existing Region.

    At first update a Region with a set of BlockStorage Services,
    updating its attributes and removing the services.

    Update a Region with no BlockStorage services, changing its
    attributes and linking a new BlockStorage service.

    Update a Region with a set of BlockStorage services, changing both
    its attributes and replacing the services with a new ones.

    Update a Region with a set of BlockStorage services, changing only
    its attributes leaving untouched its connections (this is different
    from the previous test because the flag force is set to True).
    """
    project.create(obj_in=create_random_project(), provider=db_provider)

    item_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)

    block_storage_services = item_in.block_storage_services
    item_in = create_random_region()
    item_in.block_storage_services = block_storage_services
    # Works also if projects is an empty list since,
    # in this case, nested networks are equal.
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_compute_services(
    db_provider: Provider,
) -> None:
    """Update the attributes and relationships of an existing Region.

    At first update a Region with a set of Compute Services, updating
    its attributes and removing the services.

    Update a Region with no Compute services, changing its attributes
    and linking a new Compute service.

    Update a Region with a set of Compute services, changing both its
    attributes and replacing the services with a new ones.

    Update a Region with a set of Compute services, changing only its
    attributes leaving untouched its connections (this is different from
    the previous test because the flag force is set to True).
    """
    project.create(obj_in=create_random_project(), provider=db_provider)

    item_in = create_random_region(
        with_compute_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_compute_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_compute_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)

    compute_services = item_in.compute_services
    item_in = create_random_region()
    item_in.compute_services = compute_services
    # Works also if projects is an empty list since,
    # in this case, nested networks are equal.
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_identity_services(
    db_provider: Provider,
) -> None:
    """Update the attributes and relationships of an existing Region.

    At first update a Region with a identity service, updating its
    attributes and removing the identity service.

    Update a Region with no projects, changing its attributes and
    linking a new identity service.

    Update a Region with a identity service, changing both its
    attributes and replacing the identity service with a new one.

    Update a Region with a identity service, changing only its
    attributes leaving untouched its connections (this is different from
    the previous test because the flag force is set to True).
    """
    item_in = create_random_region(with_identity_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(with_identity_services=True)
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(with_identity_services=True)
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    identity_services = item_in.identity_services
    item_in = create_random_region()
    item_in.identity_services = identity_services
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_network_services(
    db_provider: Provider,
) -> None:
    """Update the attributes and relationships of an existing Region.

    At first update a Region with a set of Network Services, updating
    its attributes and removing the services.

    Update a Region with no Network services, changing its attributes
    and linking a new Network service.

    Update a Region with a set of Network services, changing both its
    attributes and replacing the services with a new ones.

    Update a Region with a set of Network services, changing only its
    attributes leaving untouched its connections (this is different from
    the previous test because the flag force is set to True).
    """
    project.create(obj_in=create_random_project(), provider=db_provider)

    item_in = create_random_region(
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)

    network_services = item_in.network_services
    item_in = create_random_region()
    item_in.network_services = network_services
    # Works also if projects is an empty list since,
    # in this case, nested networks are equal.
    item = region.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_region_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_provider: Provider) -> None:
    """Delete an existing Region."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    result = region.remove(db_obj=item)
    assert result
    item = region.get(uid=item.uid)
    assert not item
    assert db_provider


def test_delete_item_with_relationships(db_provider: Provider) -> None:
    """Delete an existing Region.

    On Cascade delete all linked services. Delete location only if there
    are no more regions linked to it.
    """
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    item_in = create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    db_location = item.location.single()
    db_services = item.services.all()

    result = region.remove(db_obj=item)
    assert result
    item = region.get(uid=item.uid)
    assert not item
    item = location.get(uid=db_location.uid)
    assert not item
    for db_service in db_services:
        if db_service.type == ServiceType.BLOCK_STORAGE:
            item = block_storage_service.get(uid=db_service.uid)
        if db_service.type == ServiceType.COMPUTE:
            item = compute_service.get(uid=db_service.uid)
        if db_service.type == ServiceType.IDENTITY:
            item = identity_service.get(uid=db_service.uid)
        if db_service.type == ServiceType.NETWORK:
            item = network_service.get(uid=db_service.uid)
        assert item is None


def test_failed_delete_item(db_provider: Provider) -> None:
    """Try to delete the unique Region of a Provider."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    result = region.remove(db_obj=item)
    assert not result
    item = region.get(uid=item.uid)
    validate_region_attrs(obj_in=item_in, db_item=item)
