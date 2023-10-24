from uuid import uuid4

from app.network.crud import network
from app.project.crud import project
from app.service.models import NetworkService
from app.tests.utils.network import (
    create_random_network,
    create_random_network_patch,
    validate_create_network_attrs,
)
from app.tests.utils.project import create_random_project


def test_create_item(db_network_serv: NetworkService) -> None:
    """Create a Network belonging to a specific Network Service."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    validate_create_network_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_network_serv: NetworkService) -> None:
    """Create a Network, with default values when possible, belonging to a
    specific Network Service."""
    item_in = create_random_network(default=True)
    item = network.create(obj_in=item_in, service=db_network_serv)
    validate_create_network_attrs(obj_in=item_in, db_item=item)


def test_create_item_private(db_network_serv: NetworkService) -> None:
    """Create a private Network belonging to a specific Network Service.

    Private Networks requires a unique allowed project.
    """
    db_region = db_network_serv.region.single()
    db_provider = db_region.provider.single()
    project = db_provider.projects.all()[0]
    item_in = create_random_network(project=project.uuid)
    item = network.create(obj_in=item_in, service=db_network_serv, project=project)
    validate_create_network_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_network_serv: NetworkService) -> None:
    """Retrieve a Network from its UID."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    item = network.get(uid=item.uid)
    validate_create_network_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_network_serv: NetworkService) -> None:
    """Try to retrieve a not existing Network."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    item = network.get(uid=uuid4())
    assert not item


def test_get_items(db_network_serv: NetworkService) -> None:
    """Retrieve multiple networks."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    item_in2 = create_random_network()
    item2 = network.create(obj_in=item_in2, service=db_network_serv)

    stored_items = network.get_multi()
    assert len(stored_items) == 2

    stored_items = network.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_create_network_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = network.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_create_network_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_network_serv: NetworkService) -> None:
    """Test the 'limit' attribute in GET operations."""
    item_in = create_random_network()
    network.create(obj_in=item_in, service=db_network_serv)
    item_in2 = create_random_network()
    network.create(obj_in=item_in2, service=db_network_serv)

    stored_items = network.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = network.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = network.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_network_serv: NetworkService) -> None:
    """Test the 'sort' attribute in GET operations."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    item_in2 = create_random_network()
    item2 = network.create(obj_in=item_in2, service=db_network_serv)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = network.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = network.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_network_serv: NetworkService) -> None:
    """Test the 'skip' attribute in GET operations."""
    item_in = create_random_network()
    network.create(obj_in=item_in, service=db_network_serv)
    item_in2 = create_random_network()
    network.create(obj_in=item_in2, service=db_network_serv)

    stored_items = network.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = network.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_network_serv: NetworkService) -> None:
    """Update the attributes of an existing Network, without updating its
    relationships."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    patch_in = create_random_network_patch()
    patch_in.is_shared = item.is_shared
    item = network.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_network_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_network_serv: NetworkService) -> None:
    """Try to update the attributes of an existing Network, without updating
    its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    patch_in = create_random_network_patch(default=True)
    assert not network.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_network_patch(default=True)
    patch_in.description = ""
    patch_in.is_shared = item.is_shared
    item = network.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_network_attrs(obj_in=item_in, db_item=item)


# TODO try to patch network setting it as private when there are no projects
# or public when it has related projects


def test_forced_update_item(db_network_serv: NetworkService) -> None:
    """Update the attributes and relationships of an existing Network.

    At first update a Network with a set of linked projects, updating
    its attributes and removing all linked projects.

    Update a Network with no projects, changing its attributes and
    linking a new project.

    Update a Network with a set of linked projects, changing both its
    attributes and replacing the linked projects with new ones.

    Update a Network with a set of linked projects, changing only its
    attributes leaving untouched its connections (this is different from
    the previous test because the flag force is set to True).
    """
    db_region = db_network_serv.region.single()
    db_provider = db_region.provider.single()
    project1 = db_provider.projects.all()[0]
    item_in = create_random_network(project=project1.uuid)
    item = network.create(obj_in=item_in, service=db_network_serv, project=project1)
    item_in = create_random_network()
    item = network.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_network_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_network(project=project1.uuid)
    item = network.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_network_attrs(obj_in=item_in, db_item=item)

    project2 = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_network(project=project2.uuid)
    item = network.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_network_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_network(project=item_in.project)
    item = network.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_network_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_network_serv: NetworkService) -> None:
    """Delete an existing public Network."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv)
    result = network.remove(db_obj=item)
    assert result
    item = network.get(uid=item.uid)
    assert not item
    assert db_network_serv


def test_delete_item_with_relationships(db_network_serv: NetworkService) -> None:
    """Delete an existing private Network.

    Do not delete linked projects
    """
    db_region = db_network_serv.region.single()
    db_provider = db_region.provider.single()
    project = db_provider.projects.all()[0]
    item_in = create_random_network(project=project.uuid)
    item = network.create(obj_in=item_in, service=db_network_serv, project=project)
    num_db_project = len(db_provider.projects)
    result = network.remove(db_obj=item)
    assert result
    item = network.get(uid=item.uid)
    assert not item
    assert len(db_provider.projects) == num_db_project
