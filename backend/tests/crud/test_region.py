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
    """Create a Region, with default values when possible, belonging to a
    specific Provider."""
    item_in = create_random_region(default=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_location(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with a Location."""
    item_in = create_random_region(with_location=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_already_existing_location(db_location: Location) -> None:
    """Create a Region belonging to a specific Provider with an already
    existing Location.

    At first the new region points to a location with same site name but
    different attributes.

    In the latter the new location equals the existing one.

    Verify that no new locations have been created but all regions point
    to the same.
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
    """Create a Region belonging to a specific Provider with BlockStorage
    Services.

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
    """Create a Region belonging to a specific Provider with Identity
    Services."""
    item_in = create_random_region(with_identity_services=True)
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_network_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with Network
    Services."""
    item_in = create_random_region(
        with_network_services=True, projects=[i.uuid for i in db_provider.projects]
    )
    item = region.create(obj_in=item_in, provider=db_provider)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_block_storage_services(db_provider: Provider) -> None:
    """Create a Region belonging to a specific Provider with BlockStorage
    Services.

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
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_region: Region) -> None:
    """Retrieve a Region from its UID."""
    item = region.get(uid=db_region.uid)
    assert item.uid == db_region.uid


def test_get_non_existing_item() -> None:
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


def test_patch_item(db_provider: Provider) -> None:
    """Update the attributes of an existing Region, without updating its
    relationships."""
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    patch_in = create_random_region_patch()
    item = region.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_provider: Provider) -> None:
    """Try to update the attributes of an existing Region, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_region()
    item = region.create(obj_in=item_in, provider=db_provider)
    patch_in = create_random_region_patch(default=True)
    assert not region.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_region_patch(default=True)
    patch_in.description = ""
    item = region.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_region_attrs(obj_in=item_in, db_item=item)


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
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(with_location=True)
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(with_location=True)
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    loc_in = item_in.location
    item_in = create_random_region()
    item_in.location = loc_in
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_block_storage_services(
    db_provider_with_single_project: Provider,
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
    item_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider_with_single_project)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_block_storage_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    block_storage_services = item_in.block_storage_services
    item_in = create_random_region()
    item_in.block_storage_services = block_storage_services
    # Works also if projects is an empty list since,
    # in this case, nested networks are equal.
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_compute_services(
    db_provider_with_single_project: Provider,
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
    item_in = create_random_region(
        with_compute_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider_with_single_project)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_compute_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_compute_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    compute_services = item_in.compute_services
    item_in = create_random_region()
    item_in.compute_services = compute_services
    # Works also if projects is an empty list since,
    # in this case, nested networks are equal.
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)


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
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(with_identity_services=True)
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(with_identity_services=True)
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    identity_services = item_in.identity_services
    item_in = create_random_region()
    item_in.identity_services = identity_services
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_network_services(
    db_provider_with_single_project: Provider,
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
    item_in = create_random_region(
        with_network_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.create(obj_in=item_in, provider=db_provider_with_single_project)
    item_in = create_random_region()
    item = region.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_network_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_region(
        with_network_services=True,
        projects=[i.uuid for i in db_provider_with_single_project.projects],
    )
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)

    network_services = item_in.network_services
    item_in = create_random_region()
    item_in.network_services = network_services
    # Works also if projects is an empty list since,
    # in this case, nested networks are equal.
    item = region.update(
        db_obj=item,
        obj_in=item_in,
        projects=db_provider_with_single_project.projects,
        force=True,
    )
    validate_create_region_attrs(obj_in=item_in, db_item=item)


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

    On Cascade delete all linked services. Delete location only if there
    are no more regions linked to it.
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

    On Cascade delete all linked services. Delete location only if there
    are no more regions linked to it.
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
