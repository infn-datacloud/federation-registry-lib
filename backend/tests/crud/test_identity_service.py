from uuid import uuid4

from app.region.models import Region
from app.service.crud import identity_service
from app.service.models import IdentityService
from tests.utils.identity_service import (
    create_random_identity_service,
    create_random_identity_service_patch,
    validate_create_identity_service_attrs,
)


def test_create_item(db_region: Region) -> None:
    """Create an Identity Service belonging to a specific Region."""
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region)
    validate_create_identity_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_region: Region) -> None:
    """Create an Identity Service, with default values when possible, belonging
    to a specific Compute Service."""
    item_in = create_random_identity_service(default=True)
    item = identity_service.create(obj_in=item_in, region=db_region)
    validate_create_identity_service_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_identity_serv: IdentityService) -> None:
    """Retrieve an Identity Service from its UID."""
    item = identity_service.get(uid=db_identity_serv.uid)
    assert item.uid == db_identity_serv.uid


def test_get_non_existing_item() -> None:
    """Try to retrieve a not existing Identity Service."""
    assert not identity_service.get(uid=uuid4())


def test_get_items(
    db_identity_serv: IdentityService, db_identity_serv2: IdentityService
) -> None:
    """Retrieve multiple Identity Services."""
    stored_items = identity_service.get_multi()
    assert len(stored_items) == 2

    stored_items = identity_service.get_multi(uid=db_identity_serv.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_identity_serv.uid

    stored_items = identity_service.get_multi(uid=db_identity_serv2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_identity_serv2.uid


def test_get_items_with_limit(
    db_identity_serv: IdentityService, db_identity_serv2: IdentityService
) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = identity_service.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = identity_service.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = identity_service.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(
    db_identity_serv: IdentityService, db_identity_serv2: IdentityService
) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = list(sorted(identity_service.get_multi(), key=lambda x: x.uid))

    stored_items = identity_service.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = identity_service.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(
    db_identity_serv: IdentityService, db_identity_serv2: IdentityService
) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = identity_service.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = identity_service.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_region: Region) -> None:
    """Update the attributes of an existing Identity Service."""
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region)
    patch_in = create_random_identity_service_patch()
    item = identity_service.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_identity_service_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_region: Region) -> None:
    """Try to update the attributes of an existing Identity Service, without
    updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region)
    patch_in = create_random_identity_service_patch(default=True)
    assert not identity_service.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_identity_service_patch(default=True)
    patch_in.description = ""
    item = identity_service.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_identity_service_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item(db_region: Region) -> None:
    """Update the attributes of an existing Identity Service forcing default
    values when not set."""
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region)
    item_in = create_random_identity_service()
    item = identity_service.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_identity_service_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_region: Region) -> None:
    """Delete an existing Identity Service."""
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region)
    result = identity_service.remove(db_obj=item)
    assert result
    item = identity_service.get(uid=item.uid)
    assert not item
    assert db_region
