from uuid import uuid4

from app.flavor.crud import flavor
from app.image.crud import image
from app.quota.crud import compute_quota
from app.region.crud import region
from app.region.models import Region
from app.service.crud import compute_service
from app.service.models import ComputeService
from tests.utils.compute_service import (
    create_random_compute_service,
    create_random_compute_service_patch,
    validate_create_compute_service_attrs,
)


def test_create_item(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_region: Region) -> None:
    """Create a Compute Service, with default values when possible, belonging
    to a specific Region."""
    item_in = create_random_compute_service(default=True)
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region with quotas."""
    db_provider = db_region.provider.single()
    item_in = create_random_compute_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    item = compute_service.create(
        obj_in=item_in, region=db_region, projects=db_provider.projects
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_flavors(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region with flavors."""
    item_in = create_random_compute_service(with_flavors=True)
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_images(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region with images."""
    item_in = create_random_compute_service(with_images=True)
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


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
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_compute_serv: ComputeService) -> None:
    """Retrieve a Compute Service from its UID."""
    item = compute_service.get(uid=db_compute_serv.uid)
    assert item.uid == db_compute_serv.uid


def test_get_non_existing_item() -> None:
    """Try to retrieve a not existing Compute Service."""
    assert not compute_service.get(uid=uuid4())


def test_get_items(
    db_compute_serv: ComputeService, db_compute_serv2: ComputeService
) -> None:
    """Retrieve multiple Compute Services."""
    stored_items = compute_service.get_multi()
    assert len(stored_items) == 2

    stored_items = compute_service.get_multi(uid=db_compute_serv.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_compute_serv.uid

    stored_items = compute_service.get_multi(uid=db_compute_serv2.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == db_compute_serv2.uid


def test_get_items_with_limit(
    db_compute_serv: ComputeService, db_compute_serv2: ComputeService
) -> None:
    """Test the 'limit' attribute in GET operations."""
    stored_items = compute_service.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = compute_service.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = compute_service.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(
    db_compute_serv: ComputeService, db_compute_serv2: ComputeService
) -> None:
    """Test the 'sort' attribute in GET operations."""
    sorted_items = list(sorted(compute_service.get_multi(), key=lambda x: x.uid))

    stored_items = compute_service.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = compute_service.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(
    db_compute_serv: ComputeService, db_compute_serv2: ComputeService
) -> None:
    """Test the 'skip' attribute in GET operations."""
    stored_items = compute_service.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = compute_service.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_compute_serv: ComputeService) -> None:
    """Update the attributes of an existing Compute Service, without updating
    its relationships."""
    patch_in = create_random_compute_service_patch()
    item = compute_service.update(db_obj=db_compute_serv, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_compute_serv: ComputeService) -> None:
    """Try to update the attributes of an existing Compute Service, without
    updating its relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    patch_in = create_random_compute_service_patch(default=True)
    assert not compute_service.update(db_obj=db_compute_serv, obj_in=patch_in)

    patch_in = create_random_compute_service_patch(default=True)
    patch_in.description = ""
    item = compute_service.update(db_obj=db_compute_serv, obj_in=patch_in)
    assert item.description == patch_in.description
    for k, v in db_compute_serv.__dict__.items():
        if k != "description":
            assert item.__getattribute__(k) == v


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
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_compute_service(
        with_flavors=True,
        with_images=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = compute_service.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_compute_service(
        with_flavors=True,
        with_images=True,
        projects=[i.uuid for i in db_provider.projects],
    )
    item = compute_service.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)

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
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_compute_serv: ComputeService) -> None:
    """Delete an existing Compute Service."""
    db_region = db_compute_serv.region.single()
    assert compute_service.remove(db_obj=db_compute_serv)
    assert not compute_service.get(uid=db_compute_serv.uid)
    assert region.get_multi(uid=db_region.uid)


def test_delete_item_with_flavors(
    db_compute_serv_with_single_flavor: ComputeService,
) -> None:
    """Delete an existing Compute Service and its linked flavors, images and
    flavors."""
    db_region = db_compute_serv_with_single_flavor.region.single()
    db_flavor = db_compute_serv_with_single_flavor.flavors.single()
    assert compute_service.remove(db_obj=db_compute_serv_with_single_flavor)
    assert not compute_service.get(uid=db_compute_serv_with_single_flavor.uid)
    assert region.get(uid=db_region.uid)
    assert not flavor.get(uid=db_flavor.uid)


def test_delete_item_with_images(
    db_compute_serv_with_single_image: ComputeService,
) -> None:
    """Delete an existing Compute Service and its linked flavors, images and
    images."""
    db_region = db_compute_serv_with_single_image.region.single()
    db_image = db_compute_serv_with_single_image.images.single()
    assert compute_service.remove(db_obj=db_compute_serv_with_single_image)
    assert not compute_service.get(uid=db_compute_serv_with_single_image.uid)
    assert region.get(uid=db_region.uid)
    assert not image.get(uid=db_image.uid)


def test_delete_item_with_quotas(
    db_compute_serv_with_single_quota: ComputeService,
) -> None:
    """Delete an existing Compute Service and its linked flavors, images and
    quotas."""
    db_region = db_compute_serv_with_single_quota.region.single()
    db_quota = db_compute_serv_with_single_quota.quotas.single()
    assert compute_service.remove(db_obj=db_compute_serv_with_single_quota)
    assert not compute_service.get(uid=db_compute_serv_with_single_quota.uid)
    assert region.get(uid=db_region.uid)
    assert not compute_quota.get(uid=db_quota.uid)
