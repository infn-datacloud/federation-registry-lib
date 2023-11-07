from typing import Generator
from uuid import uuid4

from app.network.crud import network
from app.region.crud import region
from app.region.models import Region
from app.service.crud import network_service
from app.service.models import NetworkService
from tests.utils.network_service import (
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
    """Create an Network Service, with default values when possible, belonging to a
    specific Compute Service.
    """
    item_in = create_random_network_service(default=True)
    item = network_service.create(obj_in=item_in, region=db_region)
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_networks(db_region: Region) -> None:
    """Create an Network Service, with default values when possible, belonging to a
    specific Compute Service, with related networks.
    """
    item_in = create_random_network_service(with_networks=True)
    item = network_service.create(obj_in=item_in, region=db_region)
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_network_serv: NetworkService) -> None:
    """Retrieve an Network Service from its UID."""
    item = network_service.get(uid=db_network_serv.uid)
    assert item.uid == db_network_serv.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    """Try to retrieve a not existing Network Service."""
    assert not network_service.get(uid=uuid4())


def test_get_items(
    db_network_serv: NetworkService, db_network_serv2: NetworkService
) -> None:
    """Retrieve multiple Network Services."""
    stored_items = network_service.get_multi()
    assert len(stored_items) == 2

    stored_items = network_service.get_multi(uid=db_network_serv.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_network_serv.uid

    stored_items = network_service.get_multi(uid=db_network_serv2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_network_serv2.uid


def test_get_items_with_limit(
    db_network_serv: NetworkService, db_network_serv2: NetworkService
) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = network_service.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = network_service.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = network_service.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(
    db_network_serv: NetworkService, db_network_serv2: NetworkService
) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = sorted(network_service.get_multi(), key=lambda x: x.uid)

    stored_items = network_service.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = network_service.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(
    db_network_serv: NetworkService, db_network_serv2: NetworkService
) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = network_service.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = network_service.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_network_serv: NetworkService) -> None:
    """Update the attributes of an existing Network Service, without updating its
    relationships.
    """
    patch_in = create_random_network_service_patch()
    item = network_service.update(db_obj=db_network_serv, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_network_serv: NetworkService) -> None:
    """Try to update the attributes of an existing Network Service, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
    """
    patch_in = create_random_network_service_patch(default=True)
    assert not network_service.update(db_obj=db_network_serv, obj_in=patch_in)

    patch_in = create_random_network_service_patch(default=True)
    patch_in.description = ""
    item = network_service.update(db_obj=db_network_serv, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_network_serv.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


def test_add_networks(db_network_serv: NetworkService) -> None:
    """Update the attributes and relationships of an existing Network Service.

    Update a Network Service with no networks, changing its attributes and linking a new
    network.
    """
    db_region = db_network_serv.region.single()
    item_in = create_random_network_service(with_networks=True)
    item = network_service.update(db_obj=db_network_serv, obj_in=item_in, force=True)
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.networks) > 0


def test_remove_networks(db_network_serv_with_single_network: NetworkService) -> None:
    """Update the attributes and relationships of an existing Network Service.

    Update a Network Service with a set of linked networks, updating its attributes and
    removing all linked networks.
    """
    db_region = db_network_serv_with_single_network.region.single()
    item_in = create_random_network_service()
    item = network_service.update(
        db_obj=db_network_serv_with_single_network, obj_in=item_in, force=True
    )
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.networks) == 0


def test_replace_public_net_with_public(
    db_network_serv_with_single_network: NetworkService,
) -> None:
    """Update the attributes and relationships of an existing Network Service.

    Update a Network Service with a set of linked networks, changing both its attributes
    and replacing the linked networks with new ones.
    """
    db_region = db_network_serv_with_single_network.region.single()
    db_network = db_network_serv_with_single_network.networks.single()
    item_in = create_random_network_service(with_networks=True)
    item = network_service.update(
        db_obj=db_network_serv_with_single_network, obj_in=item_in, force=True
    )
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.networks) == 1
    assert item.networks.single() != db_network


def test_replace_public_net_with_private(
    db_network_serv_with_single_network: NetworkService,
) -> None:
    """Update the attributes and relationships of an existing Network Service.

    Update a Network Service with a set of linked networks, changing both its attributes
    and replacing the linked networks with new ones (in this case with a private one).
    """
    db_region = db_network_serv_with_single_network.region.single()
    db_provider = db_region.provider.single()
    db_network = db_network_serv_with_single_network.networks.single()
    item_in = create_random_network_service(
        with_networks=True, projects=[i.uuid for i in db_provider.projects]
    )
    item = network_service.update(
        db_obj=db_network_serv_with_single_network,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.networks) == 1
    assert item.networks.single() != db_network
    assert item.networks.single().project


def test_force_update_without_changing_relationships(
    db_network_serv_with_single_network: NetworkService,
) -> None:
    """Update the attributes and relationships of an existing Network Service.

    Update a Network Service with a set of linked networks, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_region = db_network_serv_with_single_network.region.single()
    db_network = db_network_serv_with_single_network.networks.single()
    item_in = create_random_network_service(with_networks=True)
    for k in item_in.networks[0].dict(exclude={"project"}).keys():
        item_in.networks[0].__setattr__(k, db_network.__getattribute__(k))
    item = network_service.update(
        db_obj=db_network_serv_with_single_network, obj_in=item_in, force=True
    )
    validate_create_network_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert item.networks.single() == db_network


def test_delete_item(db_network_serv: NetworkService) -> None:
    """Delete an existing Network Service."""
    db_region = db_network_serv.region.single()
    assert network_service.remove(db_obj=db_network_serv)
    assert not network_service.get(uid=db_network_serv.uid)
    assert region.get_multi(uid=db_region.uid)


def test_delete_item_with_relationships(
    db_network_serv_with_single_network: NetworkService,
) -> None:
    """Delete an existing Network Service and its linked networks."""
    db_region = db_network_serv_with_single_network.region.single()
    db_network = db_network_serv_with_single_network.networks.single()
    assert network_service.remove(db_obj=db_network_serv_with_single_network)
    assert not network_service.get(uid=db_network_serv_with_single_network.uid)
    assert region.get_multi(uid=db_region.uid)
    assert not network.get(uid=db_network.uid)
