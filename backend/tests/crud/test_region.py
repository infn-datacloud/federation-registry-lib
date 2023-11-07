from typing import Generator
from uuid import uuid4

from app.location.crud import location
from app.location.models import Location
from app.provider.crud import provider
from app.provider.models import Provider
from app.region.crud import region
from app.region.models import Region
from app.service.crud import (
    block_storage_service,
    compute_service,
    identity_service,
    network_service,
)
from tests.utils.region import (
    create_random_region,
    create_random_region_patch,
    validate_create_region_attrs,
)


def test_create_item(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_provider: Provider) -> None:
    """Create a Region, with default values when possible, belonging to a specific
    Provider.
    """
    item_in = create_random_region(default=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_location(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with a Location."""
    item_in = create_random_region(with_location=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_already_existing_location(db_location: Location) -> None:
    """Create a Region belonging to a specific Provider with an already existing
    Location.

    At first the new region points to a location with same site name but different
    attributes.

    In the latter the new location equals the existing one.

    Verify that no new locations have been created but all regions point to the same.
    """
    db_region = db_location.regions.single()
    db_provider = db_region.provider.single()

    item_in = create_random_region(with_location=True)
    item_in.location.site = db_location.site
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    loc_in = item_in.location
    item_in = create_random_region()
    item_in.location = loc_in
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    assert len(location.get_multi()) == 1


def test_create_item_with_projects_and_block_storage_services(
    db_provider: Provider,
) -> None:
    """Create a Region belonging to a specific Provider with BlockStorage Services.

    On Cascade create related quotas
    """
    item_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_compute_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Compute Services.

    On Cascade create related quotas
    """
    item_in = create_random_region(
        with_compute_services=True, projects=[i.uuid for i in db_provider.projects]
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_identity_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Identity Services."""
    item_in = create_random_region(with_identity_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_network_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Network Services."""
    item_in = create_random_region(
        with_network_services=True, projects=[i.uuid for i in db_provider.projects]
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_block_storage_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with BlockStorage Services.

    No quotas
    """
    item_in = create_random_region(with_block_storage_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_compute_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Compute Services.

    No quotas
    """
    item_in = create_random_region(with_compute_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_network_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Compute Services.

    Only public networks
    """
    item_in = create_random_region(with_network_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_everything(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Location, BlockStorage
    Services, Compute Services, Identity Services and Network Services.
    """
    item_in = create_random_region(
        with_location=True,
        with_block_storage_services=True,
        with_compute_services=True,
        with_identity_services=True,
        with_network_services=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_region: Region) -> None:
    """Retrieve a Region from its UID."""
    item = region.get(uid=db_region.uid)
    assert item.uid == db_region.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing Region."""
    assert not region.get(uid=uuid4())


def test_get_items(db_region: Region, db_region2: Region) -> None:
    """Retrieve multiple Regions."""
    stored_items = region.get_multi()
    assert len(stored_items) == 2

    stored_items = region.get_multi(uid=db_region.uid)
    assert len(stored_items) == 1

    stored_items = region.get_multi(uid=db_region2.uid)
    assert len(stored_items) == 1


def test_get_items_with_limit(db_region: Region, db_region2: Region) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = region.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = region.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = region.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_region: Region, db_region2: Region) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = list(sorted(region.get_multi(), key=lambda x: x.uid))

    stored_items = region.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = region.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_region: Region, db_region2: Region) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = region.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = region.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_region: Region) -> None:
    """Update the attributes of an existing Region, without updating its
    relationships.
    """
    patch_in = create_random_region_patch()
    item = region.update(db_obj=db_region, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_region: Region) -> None:
    """Try to update the attributes of an existing Region, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
    """
    patch_in = create_random_region_patch(default=True)
    assert not region.update(db_obj=db_region, obj_in=patch_in)

    patch_in = create_random_region_patch(default=True)
    patch_in.description = ""
    item = region.update(db_obj=db_region, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_region.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_add_location(db_region: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with no locations, changing its attributes and linking a new
    location.
    """
    db_provider = db_region.provider.single()
    item_in = create_random_region(with_location=True)
    item = region.update(db_obj=db_region, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.location) > 0


def test_remove_location(db_region_with_location: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked locations, updating its attributes and removing
    all linked locations.
    """
    db_provider = db_region_with_location.provider.single()
    item_in = create_random_region()
    item = region.update(db_obj=db_region_with_location, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.location) == 0


def test_remove_shared_location(db_region_with_shared_location: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked locations, updating its attributes and removing
    all linked locations.
    """
    db_provider = db_region_with_shared_location.provider.single()
    db_location = db_region_with_shared_location.location.single()
    item_in = create_random_region()
    item = region.update(
        db_obj=db_region_with_shared_location, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.location) == 0
    assert location.get(uid=db_location.uid)


def test_replace_locations(db_region_with_location: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked locations, changing both its attributes and
    replacing the linked locations with new ones.
    """
    db_provider = db_region_with_location.provider.single()
    db_location = db_region_with_location.location.single()
    item_in = create_random_region(with_location=True)
    item = region.update(db_obj=db_region_with_location, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.location) == 1
    assert item.location.single() != db_location


def test_force_update_without_changing_locations(
    db_region_with_location: Region,
) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked locations, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_provider = db_region_with_location.provider.single()
    db_location = db_region_with_location.location.single()
    item_in = create_random_region(with_location=True)
    for k in item_in.location.dict().keys():
        item_in.location.__setattr__(k, db_location.__getattribute__(k))
    item = region.update(db_obj=db_region_with_location, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.location.single() == db_location


def test_add_block_storage_service(db_region: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with no block_storage_services, changing its attributes and linking
    a new block_storage_service.
    """
    db_provider = db_region.provider.single()
    item_in = create_random_region(with_block_storage_services=True)
    item = region.update(db_obj=db_region, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) > 0


def test_remove_block_storage_service(
    db_region_with_block_storage_service: Region,
) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked block_storage_services, updating its attributes
    and removing all linked block_storage_services.
    """
    db_provider = db_region_with_block_storage_service.provider.single()
    item_in = create_random_region()
    item = region.update(
        db_obj=db_region_with_block_storage_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) == 0


def test_replace_block_storage_services(
    db_region_with_block_storage_service: Region,
) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked block_storage_services, changing both its
    attributes and replacing the linked block_storage_services with new ones.
    """
    db_provider = db_region_with_block_storage_service.provider.single()
    db_service = db_region_with_block_storage_service.services.single()
    item_in = create_random_region(with_block_storage_services=True)
    item = region.update(
        db_obj=db_region_with_block_storage_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) == 1
    assert item.services.single() != db_service


def test_force_update_without_changing_block_storage_services(
    db_region_with_block_storage_service: Region,
) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked block_storage_services, changing only its
    attributes leaving untouched its connections (this is different from the previous
    test because the flag force is set to True).
    """
    db_provider = db_region_with_block_storage_service.provider.single()
    db_service = db_region_with_block_storage_service.services.single()
    item_in = create_random_region(with_block_storage_services=True)
    for k in item_in.block_storage_services[0].dict(exclude={"quotas"}).keys():
        item_in.block_storage_services[0].__setattr__(k, db_service.__getattribute__(k))
    item = region.update(
        db_obj=db_region_with_block_storage_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.services.single() == db_service


def test_add_compute_service(db_region: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with no compute_services, changing its attributes and linking a new
    compute_service.
    """
    db_provider = db_region.provider.single()
    item_in = create_random_region(with_compute_services=True)
    item = region.update(db_obj=db_region, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) > 0


def test_remove_compute_service(db_region_with_compute_service: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked compute_services, updating its attributes and
    removing all linked compute_services.
    """
    db_provider = db_region_with_compute_service.provider.single()
    item_in = create_random_region()
    item = region.update(
        db_obj=db_region_with_compute_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) == 0


def test_replace_compute_services(db_region_with_compute_service: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked compute_services, changing both its attributes
    and replacing the linked compute_services with new ones.
    """
    db_provider = db_region_with_compute_service.provider.single()
    db_service = db_region_with_compute_service.services.single()
    item_in = create_random_region(with_compute_services=True)
    item = region.update(
        db_obj=db_region_with_compute_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) == 1
    assert item.services.single() != db_service


def test_force_update_without_changing_compute_services(
    db_region_with_compute_service: Region,
) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked compute_services, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_provider = db_region_with_compute_service.provider.single()
    db_service = db_region_with_compute_service.services.single()
    item_in = create_random_region(with_compute_services=True)
    for k in (
        item_in.compute_services[0].dict(exclude={"flavors", "images", "quotas"}).keys()
    ):
        item_in.compute_services[0].__setattr__(k, db_service.__getattribute__(k))
    item = region.update(
        db_obj=db_region_with_compute_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.services.single() == db_service


def test_add_identity_service(db_region: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with no identity_services, changing its attributes and linking a new
    identity_service.
    """
    db_provider = db_region.provider.single()
    item_in = create_random_region(with_identity_services=True)
    item = region.update(db_obj=db_region, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) > 0


def test_remove_identity_service(db_region_with_identity_service: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked identity_services, updating its attributes and
    removing all linked identity_services.
    """
    db_provider = db_region_with_identity_service.provider.single()
    item_in = create_random_region()
    item = region.update(
        db_obj=db_region_with_identity_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) == 0


def test_replace_identity_services(db_region_with_identity_service: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked identity_services, changing both its attributes
    and replacing the linked identity_services with new ones.
    """
    db_provider = db_region_with_identity_service.provider.single()
    db_service = db_region_with_identity_service.services.single()
    item_in = create_random_region(with_identity_services=True)
    item = region.update(
        db_obj=db_region_with_identity_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) == 1
    assert item.services.single() != db_service


def test_force_update_without_changing_identity_services(
    db_region_with_identity_service: Region,
) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked identity_services, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_provider = db_region_with_identity_service.provider.single()
    db_service = db_region_with_identity_service.services.single()
    item_in = create_random_region(with_identity_services=True)
    for k in item_in.identity_services[0].dict().keys():
        item_in.identity_services[0].__setattr__(k, db_service.__getattribute__(k))
    item = region.update(
        db_obj=db_region_with_identity_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.services.single() == db_service


def test_add_network_service(db_region: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with no network_services, changing its attributes and linking a new
    network_service.
    """
    db_provider = db_region.provider.single()
    item_in = create_random_region(with_network_services=True)
    item = region.update(db_obj=db_region, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) > 0


def test_remove_network_service(db_region_with_network_service: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked network_services, updating its attributes and
    removing all linked network_services.
    """
    db_provider = db_region_with_network_service.provider.single()
    item_in = create_random_region()
    item = region.update(
        db_obj=db_region_with_network_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) == 0


def test_replace_network_services(db_region_with_network_service: Region) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked network_services, changing both its attributes
    and replacing the linked network_services with new ones.
    """
    db_provider = db_region_with_network_service.provider.single()
    db_service = db_region_with_network_service.services.single()
    item_in = create_random_region(with_network_services=True)
    item = region.update(
        db_obj=db_region_with_network_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert len(item.services) == 1
    assert item.services.single() != db_service


def test_force_update_without_changing_network_services(
    db_region_with_network_service: Region,
) -> None:
    """Update the attributes and relationships of an existing Region.

    Update a Region with a set of linked network_services, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_provider = db_region_with_network_service.provider.single()
    db_service = db_region_with_network_service.services.single()
    item_in = create_random_region(with_network_services=True)
    for k in item_in.network_services[0].dict(exclude={"networks"}).keys():
        item_in.network_services[0].__setattr__(k, db_service.__getattribute__(k))
    item = region.update(
        db_obj=db_region_with_network_service, obj_in=item_in, force=True
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)
    assert item.provider.single() == db_provider
    assert item.services.single() == db_service


def test_delete_item(db_region3: Region) -> None:
    """Delete an existing Region."""
    db_provider = db_region3.provider.single()
    assert region.remove(db_obj=db_region3)
    assert not region.get(uid=db_region3.uid)
    assert provider.get(uid=db_provider.uid)


def test_failed_delete_item(db_region: Region) -> None:
    """Try to delete the unique Region of a Provider."""
    db_provider = db_region.provider.single()
    assert not region.remove(db_obj=db_region)
    assert region.get(uid=db_region.uid)
    assert provider.get(uid=db_provider.uid)


def test_delete_item_with_proprietary_location(
    db_deletable_region_with_location: Region,
) -> None:
    """Delete an existing Region.

    On Cascade delete all linked services. Delete location only if there are no more
    regions linked to it.
    """
    db_provider = db_deletable_region_with_location.provider.single()
    db_location = db_deletable_region_with_location.location.single()
    assert region.remove(db_obj=db_deletable_region_with_location)
    assert not region.get(uid=db_deletable_region_with_location.uid)
    assert provider.get(uid=db_provider.uid)
    assert not location.get(uid=db_location.uid)


def test_delete_item_with_shared_location(
    db_region_with_shared_location: Region,
) -> None:
    """Delete an existing Region.

    On Cascade delete all linked services. Delete location only if there are no more
    regions linked to it.
    """
    db_provider = db_region_with_shared_location.provider.single()
    db_location = db_region_with_shared_location.location.single()
    assert region.remove(db_obj=db_region_with_shared_location)
    assert not region.get(uid=db_region_with_shared_location.uid)
    assert provider.get(uid=db_provider.uid)
    assert location.get(uid=db_location.uid)


def test_failed_delete_item_with_proprietary_location(
    db_region_with_location: Region,
) -> None:
    """Try to delete the unique Region of a Provider.

    Location is still there.
    """
    db_provider = db_region_with_location.provider.single()
    db_location = db_region_with_location.location.single()
    assert not region.remove(db_obj=db_region_with_location)
    assert region.get(uid=db_region_with_location.uid)
    assert provider.get(uid=db_provider.uid)
    assert location.get(uid=db_location.uid)


def test_delete_item_with_block_storage_service(
    db_deletable_region_with_block_storage_service: Region,
) -> None:
    """Delete an existing Region.

    On Cascade delete all linked services.
    """
    db_provider = db_deletable_region_with_block_storage_service.provider.single()
    db_service = db_deletable_region_with_block_storage_service.services.single()
    assert region.remove(db_obj=db_deletable_region_with_block_storage_service)
    assert not region.get(uid=db_deletable_region_with_block_storage_service.uid)
    assert provider.get(uid=db_provider.uid)
    assert not block_storage_service.get(uid=db_service.uid)


def test_failed_delete_item_with_block_storage_service(
    db_region_with_block_storage_service: Region,
) -> None:
    """Try to delete the unique Region of a Provider.

    Service is still there.
    """
    db_provider = db_region_with_block_storage_service.provider.single()
    db_service = db_region_with_block_storage_service.services.single()
    assert not region.remove(db_obj=db_region_with_block_storage_service)
    assert region.get(uid=db_region_with_block_storage_service.uid)
    assert provider.get(uid=db_provider.uid)
    assert block_storage_service.get(uid=db_service.uid)


def test_delete_item_with_compute_service(
    db_deletable_region_with_compute_service: Region,
) -> None:
    """Delete an existing Region.

    On Cascade delete all linked services.
    """
    db_provider = db_deletable_region_with_compute_service.provider.single()
    db_service = db_deletable_region_with_compute_service.services.single()
    assert region.remove(db_obj=db_deletable_region_with_compute_service)
    assert not region.get(uid=db_deletable_region_with_compute_service.uid)
    assert provider.get(uid=db_provider.uid)
    assert not compute_service.get(uid=db_service.uid)


def test_failed_delete_item_with_compute_service(
    db_region_with_compute_service: Region,
) -> None:
    """Try to delete the unique Region of a Provider.

    Service is still there.
    """
    db_provider = db_region_with_compute_service.provider.single()
    db_service = db_region_with_compute_service.services.single()
    assert not region.remove(db_obj=db_region_with_compute_service)
    assert region.get(uid=db_region_with_compute_service.uid)
    assert provider.get(uid=db_provider.uid)
    assert compute_service.get(uid=db_service.uid)


def test_delete_item_with_identity_service(
    db_deletable_region_with_identity_service: Region,
) -> None:
    """Delete an existing Region.

    On Cascade delete all linked services.
    """
    db_provider = db_deletable_region_with_identity_service.provider.single()
    db_service = db_deletable_region_with_identity_service.services.single()
    assert region.remove(db_obj=db_deletable_region_with_identity_service)
    assert not region.get(uid=db_deletable_region_with_identity_service.uid)
    assert provider.get(uid=db_provider.uid)
    assert not identity_service.get(uid=db_service.uid)


def test_failed_delete_item_with_identity_service(
    db_region_with_identity_service: Region,
) -> None:
    """Try to delete the unique Region of a Provider.

    Service is still there.
    """
    db_provider = db_region_with_identity_service.provider.single()
    db_service = db_region_with_identity_service.services.single()
    assert not region.remove(db_obj=db_region_with_identity_service)
    assert region.get(uid=db_region_with_identity_service.uid)
    assert provider.get(uid=db_provider.uid)
    assert identity_service.get(uid=db_service.uid)


def test_delete_item_with_network_service(
    db_deletable_region_with_network_service: Region,
) -> None:
    """Delete an existing Region.

    On Cascade delete all linked services.
    """
    db_provider = db_deletable_region_with_network_service.provider.single()
    db_service = db_deletable_region_with_network_service.services.single()
    assert region.remove(db_obj=db_deletable_region_with_network_service)
    assert not region.get(uid=db_deletable_region_with_network_service.uid)
    assert provider.get(uid=db_provider.uid)
    assert not network_service.get(uid=db_service.uid)


def test_failed_delete_item_with_network_service(
    db_region_with_network_service: Region,
) -> None:
    """Try to delete the unique Region of a Provider.

    Service is still there.
    """
    db_provider = db_region_with_network_service.provider.single()
    db_service = db_region_with_network_service.services.single()
    assert not region.remove(db_obj=db_region_with_network_service)
    assert region.get(uid=db_region_with_network_service.uid)
    assert provider.get(uid=db_provider.uid)
    assert network_service.get(uid=db_service.uid)
