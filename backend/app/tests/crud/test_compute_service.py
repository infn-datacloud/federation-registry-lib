from uuid import uuid4

from app.flavor.crud import flavor
from app.image.crud import image
from app.quota.crud import compute_quota
from app.region.models import Region
from app.service.crud import compute_service
from app.tests.utils.service import (
    create_random_compute_service,
    create_random_compute_service_patch,
    validate_compute_service_attrs,
)


def test_create_item(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_region: Region) -> None:
    """Create a Compute Service, with default values when possible, belonging
    to a specific Region."""
    item_in = create_random_compute_service(default=True)
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region with quotas."""
    db_provider = db_region.provider.single()
    item_in = create_random_compute_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = compute_service.create(
        obj_in=item_in, region=db_region, projects=db_provider.projects
    )
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_flavors(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region with flavors."""
    item_in = create_random_compute_service(with_flavors=True)
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_images(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region with images."""
    item_in = create_random_compute_service(with_images=True)
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_everything(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region with flavors,
    images and quotas."""
    db_provider = db_region.provider.single()
    item_in = create_random_compute_service(
        with_flavors=True,
        with_images=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = compute_service.create(
        obj_in=item_in, region=db_region, projects=db_provider.projects
    )
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_region: Region) -> None:
    """Retrieve a Compute Service from its UID."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    item = compute_service.get(uid=item.uid)
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(db_region: Region) -> None:
    """Try to retrieve a not existing Compute Service."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    item = compute_service.get(uid=uuid4())
    assert not item


def test_get_items(db_region: Region) -> None:
    """Retrieve multiple Compute Services."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_compute_service()
    item2 = compute_service.create(obj_in=item_in2, region=db_region)

    stored_items = compute_service.get_multi()
    assert len(stored_items) == 2

    stored_items = compute_service.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_compute_service_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = compute_service.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_compute_service_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_region: Region) -> None:
    """Test the 'limit' attribute in GET operations."""
    item_in = create_random_compute_service()
    compute_service.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_compute_service()
    compute_service.create(obj_in=item_in2, region=db_region)

    stored_items = compute_service.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = compute_service.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = compute_service.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_region: Region) -> None:
    """Test the 'sort' attribute in GET operations."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_compute_service()
    item2 = compute_service.create(obj_in=item_in2, region=db_region)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = compute_service.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = compute_service.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_region: Region) -> None:
    """Test the 'skip' attribute in GET operations."""
    item_in = create_random_compute_service()
    compute_service.create(obj_in=item_in, region=db_region)
    item_in2 = create_random_compute_service()
    compute_service.create(obj_in=item_in2, region=db_region)

    stored_items = compute_service.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = compute_service.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_region: Region) -> None:
    """Update the attributes of an existing Compute Service, without updating
    its relationships."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    patch_in = create_random_compute_service_patch()
    item = compute_service.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_region: Region) -> None:
    """Try to update the attributes of an existing Compute Service, without
    updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    patch_in = create_random_compute_service_patch(default=True)
    assert not compute_service.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_compute_service_patch(default=True)
    patch_in.description = ""
    item = compute_service.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_(db_region: Region) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    At first update a Compute Service with a set of linked projects,
    updating its attributes and removing all linked projects.

    Update a Compute Service with no projects, changing its attributes
    and linking a new project.

    Update a Compute Service with a set of linked projects, changing
    both its attributes and replacing the linked projects with new ones.

    Update a Compute Service with a set of linked projects, changing
    only its attributes leaving untouched its connections (this is
    different from the previous test because the flag force is set to
    True).
    """
    db_provider = db_region.provider.single()
    item_in = create_random_compute_service(
        with_flavors=True,
        with_images=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = compute_service.create(
        obj_in=item_in, region=db_region, projects=db_provider.projects
    )
    item_in = create_random_compute_service()
    item = compute_service.update(db_obj=item, obj_in=item_in, force=True)
    validate_compute_service_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_compute_service(
        with_flavors=True,
        with_images=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = compute_service.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_compute_service_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_compute_service(
        with_flavors=True,
        with_images=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = compute_service.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_compute_service_attrs(obj_in=item_in, db_item=item)

    flavors = item_in.flavors
    images = item_in.images
    quotas = item_in.quotas
    item_in = create_random_compute_service()
    item_in.flavors = flavors
    item_in.images = images
    item_in.quotas = quotas
    item = compute_service.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_compute_service_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_region: Region) -> None:
    """Delete an existing Compute Service."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    result = compute_service.remove(db_obj=item)
    assert result
    item = compute_service.get(uid=item.uid)
    assert not item
    assert db_region


def test_delete_item_with_relationships(db_region: Region) -> None:
    """Delete an existing Compute Service and its linked flavors, images and
    quotas."""
    db_provider = db_region.provider.single()
    item_in = create_random_compute_service(
        with_flavors=True,
        with_images=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = compute_service.create(
        obj_in=item_in, region=db_region, projects=db_provider.projects
    )
    db_flavor = item.flavors.all()[0]
    db_image = item.images.all()[0]
    db_quota = item.quotas.all()[0]

    result = compute_service.remove(db_obj=item)
    assert result
    item = compute_service.get(uid=item.uid)
    assert not item
    item = flavor.get(uid=db_flavor.uid)
    assert not item
    item = image.get(uid=db_image.uid)
    assert not item
    item = compute_quota.get(uid=db_quota.uid)
    assert not item
