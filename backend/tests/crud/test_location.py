from typing import Generator
from uuid import uuid4

from app.location.crud import location
from app.location.models import Location
from app.region.crud import region
from app.region.models import Region
from tests.utils.location import (
    create_random_location,
    create_random_location_patch,
    validate_create_location_attrs,
)


def test_create_item(db_region: Region) -> None:
    """Create a Location belonging to a specific Region."""
    item_in = create_random_location()
    item = location.create(obj_in=item_in, region=db_region)
    validate_create_location_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_region: Region) -> None:
    """Create a Location, with default values when possible, belonging to a specific
    Region.
    """
    item_in = create_random_location(default=True)
    item = location.create(obj_in=item_in, region=db_region)
    validate_create_location_attrs(obj_in=item_in, db_item=item)


def test_create_when_site_already_exists(db_location: Location) -> None:
    """Try to create a Location belonging to a specific Region, when a Location with the
    same site name already exists.

    At first create a location with new attributes but same site name of existing one.
    The result will have the attributes of the new one.

    Then create a location with default values, except one, and same site name of
    existing one. The result will keep the previous attributes instead of defaults and
    update the new given attributes.

    Finally create a location with everything equal to the existing one. No changes.
    """
    db_region = db_location.regions.single()

    item_in = create_random_location()
    item_in.site = db_location.site
    item = location.create(obj_in=item_in, region=db_region)
    validate_create_location_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_location(default=True)
    item_in.site = item.site
    item = location.create(obj_in=item_in, region=db_region)
    item_in.description = item.description
    item_in.latitude = item.latitude
    item_in.longitude = item.longitude
    validate_create_location_attrs(obj_in=item_in, db_item=item)

    item = location.create(obj_in=item_in, region=db_region)
    validate_create_location_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_location: Location) -> None:
    """Retrieve a Location from its UID."""
    item = location.get(uid=db_location.uid)
    assert item.uid == db_location.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing Location."""
    assert not location.get(uid=uuid4())


def test_get_items(db_location: Location, db_location2: Location) -> None:
    """Retrieve multiple Locations."""
    stored_items = location.get_multi()
    assert len(stored_items) == 2

    stored_items = location.get_multi(uid=db_location.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_location.uid

    stored_items = location.get_multi(uid=db_location2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_location2.uid


def test_get_items_with_limit(db_location: Location, db_location2: Location) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = location.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = location.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = location.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_location: Location, db_location2: Location) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = list(sorted(location.get_multi(), key=lambda x: x.uid))

    stored_items = location.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = location.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_location: Location, db_location2: Location) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = location.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = location.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_location: Location) -> None:
    """Update the attributes of an existing Location, without updating its
    relationships.
    """
    patch_in = create_random_location_patch()
    item = location.update(db_obj=db_location, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_location: Location) -> None:
    """Try to update the attributes of an existing Location, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
    """
    patch_in = create_random_location_patch(default=True)
    assert not location.update(db_obj=db_location, obj_in=patch_in)

    patch_in = create_random_location_patch(default=True)
    patch_in.description = ""
    item = location.update(db_obj=db_location, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_location.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_force_update_without_changing_relationships(db_location: Location) -> None:
    """Update the attributes and relationships of an existing Location.

    Update a Region with a set of linked locations, changing only its attributes leaving
    untouched its connections (this is different from the previous test because the flag
    force is set to True).
    """
    db_region = db_location.regions.single()
    item_in = create_random_location()
    item = location.update(db_obj=db_location, obj_in=item_in, force=True)
    validate_create_location_attrs(obj_in=item_in, db_item=item)
    assert item.regions.single() == db_region


def test_delete_item(db_location: Location) -> None:
    """Delete an existing Location."""
    db_region = db_location.regions.single()
    assert location.remove(db_obj=db_location)
    assert not location.get(uid=db_location.uid)
    assert region.get(uid=db_region.uid)
