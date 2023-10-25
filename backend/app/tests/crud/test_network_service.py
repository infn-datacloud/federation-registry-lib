from uuid import uuid4

from app.network.crud import network
from app.region.models import Region
from app.service.crud import network_service
from app.tests.utils.network_service import (
    create_random_network_service,
    create_random_network_service_patch,
    validate_create_network_service_attrs,
)


def test_create_item(db_region: Region) -> None:
    """Create an Network Service belonging to a specific Region."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_region: Region) -> None:
    """Create an Network Service, with default values when possible, belonging
    to a specific Compute Service."""
    item_in = create_random_network_service(default=True)
    item = network_service.create(obj_in=item_in, region=db_region)
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_networks(db_region: Region) -> None:
    """Create an Network Service, with default values when possible, belonging
    to a specific Compute Service, with related networks."""
    item_in = create_random_network_service(with_networks=True)
    item = network_service.create(obj_in=item_in, region=db_region)
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_region: Region) -> None:
    """Retrieve an Network Service from its UID."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    item = network_service.get(uid=item.uid)
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_region: Region) -> None:
    """Try to retrieve a not existing Network Service."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    item = network_service.get(uid=uuid4())
    assert not item


def test_get_items(db_region: Region) -> None:
    """Retrieve multiple Network Services."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_network_service()
    item2 = network_service.create(obj_in=item_in2, region=db_region)

    stored_items = network_service.get_multi()
    assert len(stored_items) == 2

    stored_items = network_service.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_create_network_service_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = network_service.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_create_network_service_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_region: Region) -> None:
    """Test the 'limit' attribute in GET operations."""
    item_in = create_random_network_service()
    network_service.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_network_service()
    network_service.create(obj_in=item_in2, region=db_region)

    stored_items = network_service.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = network_service.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = network_service.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_region: Region) -> None:
    """Test the 'sort' attribute in GET operations."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_network_service()
    item2 = network_service.create(obj_in=item_in2, region=db_region)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = network_service.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = network_service.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_region: Region) -> None:
    """Test the 'skip' attribute in GET operations."""
    item_in = create_random_network_service()
    network_service.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_network_service()
    network_service.create(obj_in=item_in2, region=db_region)

    stored_items = network_service.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = network_service.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_region: Region) -> None:
    """Update the attributes of an existing Network Service, without updating
    its relationships."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    patch_in = create_random_network_service_patch()
    item = network_service.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_region: Region) -> None:
    """Try to update the attributes of an existing Network Service, without
    updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    patch_in = create_random_network_service_patch(default=True)
    assert not network_service.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_network_service_patch(default=True)
    patch_in.description = ""
    item = network_service.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_(db_region: Region) -> None:
    """Update the attributes and relationships of an existing Network Service.

    At first update a Network Service with a set of linked networks,
    updating its attributes and removing all linked networks.

    Update a Network Service with no networks, changing its attributes
    and linking a new network.

    Update a Network Service with a set of linked networks, changing
    both its attributes and replacing the linked networks with new ones.

    Update a Network Service with a set of linked networks, changing
    only its attributes leaving untouched its connections (this is
    different from the previous test because the flag force is set to
    True).
    """
    db_provider = db_region.provider.single()
    projects = db_provider.projects.all()
    item_in = create_random_network_service(with_networks=True)
    item = network_service.create(obj_in=item_in, region=db_region)
    item_in = create_random_network_service()
    item = network_service.update(
        db_obj=item, obj_in=item_in, projects=projects, force=True
    )
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_network_service(with_networks=True)
    item = network_service.update(
        db_obj=item, obj_in=item_in, projects=projects, force=True
    )
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_network_service(with_networks=True)
    item = network_service.update(
        db_obj=item, obj_in=item_in, projects=projects, force=True
    )
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)

    networks = item_in.networks
    item_in = create_random_network_service()
    item_in.networks = networks
    item = network_service.update(
        db_obj=item, obj_in=item_in, projects=projects, force=True
    )
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_region: Region) -> None:
    """Delete an existing Network Service."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    result = network_service.remove(db_obj=item)
    assert result
    item = network_service.get(uid=item.uid)
    assert not item
    assert db_region


def test_delete_item_with_relationships(db_region: Region) -> None:
    """Delete an existing Network Service and its linked quotas."""
    item_in = create_random_network_service(with_networks=True)
    item = network_service.create(obj_in=item_in, region=db_region)
    db_network = item.networks.all()[0]

    result = network_service.remove(db_obj=item)
    assert result
    item = network_service.get(uid=item.uid)
    assert not item
    item = network.get(uid=db_network.uid)
    assert not item
