from copy import deepcopy
from typing import Generator
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
from tests.utils.utils import random_lower_string


def test_create_item(db_region: Region) -> None:
    """Create a Compute Service belonging to a specific Region."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_region: Region) -> None:
    """Create a Compute Service, with default values when possible, belonging to a
    specific Region.
    """
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
    """Create a Compute Service belonging to a specific Region with flavors, images and
    quotas.
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
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)


def test_get_item(db_compute_serv: ComputeService) -> None:
    """Retrieve a Compute Service from its UID."""
    item = compute_service.get(uid=db_compute_serv.uid)
    assert item.uid == db_compute_serv.uid


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
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
    sorted_items = sorted(compute_service.get_multi(), key=lambda x: x.uid)

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
    """Update the attributes of an existing Compute Service, without updating its
    relationships.
    """
    patch_in = create_random_compute_service_patch()
    item = compute_service.update(db_obj=db_compute_serv, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        assert item.__getattribute__(k) == v


def test_patch_item_with_defaults(db_compute_serv: ComputeService) -> None:
    """Try to update the attributes of an existing Compute Service, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit default values,
    succeeds.
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


def test_add_quotas(db_compute_serv: ComputeService) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with no quotas, changing its attributes and linking a new
    quota.
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_compute_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    db_quota = deepcopy(item_in.quotas[0])
    db_quota.description = random_lower_string()
    db_quota.per_user = not db_quota.per_user
    item_in.quotas.append(db_quota)

    item = compute_service.update(
        db_obj=db_compute_serv,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.quotas) == 2


def test_remove_quotas(
    db_compute_serv_with_multiple_quotas: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked quotas, updating its attributes and
    removing all linked quotas.
    """
    db_region = db_compute_serv_with_multiple_quotas.region.single()
    item_in = create_random_compute_service()
    item = compute_service.update(
        db_obj=db_compute_serv_with_multiple_quotas, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.quotas) == 0


def test_replace_quotas_with_ones_pointing_to_diff_project(
    db_compute_serv_with_multiple_quotas_same_project: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked quotas, changing both its attributes
    and replacing the linked quotas with new ones.
    """
    db_region = db_compute_serv_with_multiple_quotas_same_project.region.single()
    db_provider = db_region.provider.single()
    db_quota = db_compute_serv_with_multiple_quotas_same_project.quotas.get(
        per_user=True
    )
    for db_project in db_provider.projects:
        if db_project.uid != db_quota.project.single().uid:
            break

    quotas_uids = [
        i.uid for i in db_compute_serv_with_multiple_quotas_same_project.quotas
    ]

    item_in = create_random_compute_service(projects=[db_project.uuid])
    db_quota = deepcopy(item_in.quotas[0])
    db_quota.description = random_lower_string()
    db_quota.per_user = not db_quota.per_user
    item_in.quotas.append(db_quota)

    item = compute_service.update(
        db_obj=db_compute_serv_with_multiple_quotas_same_project,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.quotas) == 2
    for i in item.quotas:
        assert i.uid not in quotas_uids


def test_replace_quotas_with_ones_pointing_to_same_project(
    db_compute_serv_with_multiple_quotas_same_project: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked quotas, changing both its attributes
    and replacing the linked quotas with new ones.
    """
    db_region = db_compute_serv_with_multiple_quotas_same_project.region.single()
    db_provider = db_region.provider.single()
    db_quota = db_compute_serv_with_multiple_quotas_same_project.quotas.get(
        per_user=True
    )
    db_project = db_quota.project.single()

    quotas_uids = [
        i.uid for i in db_compute_serv_with_multiple_quotas_same_project.quotas
    ]

    item_in = create_random_compute_service(projects=[db_project.uuid])
    db_quota = deepcopy(item_in.quotas[0])
    db_quota.description = random_lower_string()
    db_quota.per_user = not db_quota.per_user
    item_in.quotas.append(db_quota)

    item = compute_service.update(
        db_obj=db_compute_serv_with_multiple_quotas_same_project,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.quotas) == 2
    for i in sorted(item.quotas, key=lambda x: x.uid):
        assert i.uid in quotas_uids


def test_force_update_without_changing_quotas(
    db_compute_serv_with_single_quota: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked quotas, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_region = db_compute_serv_with_single_quota.region.single()
    db_provider = db_region.provider.single()
    db_quota = db_compute_serv_with_single_quota.quotas.single()
    item_in = create_random_compute_service(
        projects=[i.uuid for i in db_provider.projects]
    )
    for k in item_in.quotas[0].dict(exclude={"project"}).keys():
        item_in.quotas[0].__setattr__(k, db_quota.__getattribute__(k))
    item_in.quotas[0].project = db_quota.project.single().uuid
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_quota,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert item.quotas.single() == db_quota


def test_add_flavors(db_compute_serv: ComputeService) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with no flavors, changing its attributes and linking a new
    flavor.
    """
    db_region = db_compute_serv.region.single()
    item_in = create_random_compute_service(with_flavors=True)
    item = compute_service.update(db_obj=db_compute_serv, obj_in=item_in, force=True)
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.flavors) > 0


def test_remove_flavor(
    db_compute_serv_with_single_flavor: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked flavors, updating its attributes and
    removing all linked flavors.
    """
    db_region = db_compute_serv_with_single_flavor.region.single()
    item_in = create_random_compute_service()
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_flavor, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.flavors) == 0


def test_remove_shared_flavor(
    db_compute_serv_with_shared_flavor: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service removing a flavor which is shared between other services.
    Check that the flavor still exists.
    """
    db_region = db_compute_serv_with_shared_flavor.region.single()
    db_flavor = db_compute_serv_with_shared_flavor.flavors.single()
    item_in = create_random_compute_service()
    item = compute_service.update(
        db_obj=db_compute_serv_with_shared_flavor, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.flavors) == 0
    assert flavor.get(uid=db_flavor.uid)


def test_replace_public_flavor_with_public(
    db_compute_serv_with_single_flavor: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked flavors, changing both its attributes
    and replacing the linked flavors with new ones.
    """
    db_region = db_compute_serv_with_single_flavor.region.single()
    db_flavor = db_compute_serv_with_single_flavor.flavors.single()
    item_in = create_random_compute_service(with_flavors=True)
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_flavor, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.flavors) == 1
    assert item.flavors.single() != db_flavor


def test_replace_public_flavor_with_private(
    db_compute_serv_with_single_flavor: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked flavors, changing both its attributes
    and replacing the linked flavors with new ones (in this case with a private one).
    """
    db_region = db_compute_serv_with_single_flavor.region.single()
    db_provider = db_region.provider.single()
    db_flavor = db_compute_serv_with_single_flavor.flavors.single()
    item_in = create_random_compute_service(
        with_flavors=True, projects=[i.uuid for i in db_provider.projects]
    )
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_flavor,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.flavors) == 1
    assert item.flavors.single() != db_flavor
    assert len(item.flavors.single().projects) > 0


def test_force_update_without_changing_flavors(
    db_compute_serv_with_single_flavor: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked flavors, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_region = db_compute_serv_with_single_flavor.region.single()
    db_flavor = db_compute_serv_with_single_flavor.flavors.single()
    item_in = create_random_compute_service(with_flavors=True)
    for k in item_in.flavors[0].dict(exclude={"projects"}).keys():
        item_in.flavors[0].__setattr__(k, db_flavor.__getattribute__(k))
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_flavor, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert item.flavors.single() == db_flavor


def test_add_images(db_compute_serv: ComputeService) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with no images, changing its attributes and linking a new
    image.
    """
    db_region = db_compute_serv.region.single()
    item_in = create_random_compute_service(with_images=True)
    item = compute_service.update(db_obj=db_compute_serv, obj_in=item_in, force=True)
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.images) > 0


def test_remove_image(
    db_compute_serv_with_single_image: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked images, updating its attributes and
    removing all linked images.
    """
    db_region = db_compute_serv_with_single_image.region.single()
    item_in = create_random_compute_service()
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_image, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.images) == 0


def test_remove_shared_image(
    db_compute_serv_with_shared_image: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service removing a image which is shared between other services.
    Check that the image still exists.
    """
    db_region = db_compute_serv_with_shared_image.region.single()
    db_image = db_compute_serv_with_shared_image.images.single()
    item_in = create_random_compute_service()
    item = compute_service.update(
        db_obj=db_compute_serv_with_shared_image, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.images) == 0
    assert image.get(uid=db_image.uid)


def test_replace_public_image_with_public(
    db_compute_serv_with_single_image: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked images, changing both its attributes
    and replacing the linked images with new ones.
    """
    db_region = db_compute_serv_with_single_image.region.single()
    db_image = db_compute_serv_with_single_image.images.single()
    item_in = create_random_compute_service(with_images=True)
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_image, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.images) == 1
    assert item.images.single() != db_image


def test_replace_public_image_with_private(
    db_compute_serv_with_single_image: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked images, changing both its attributes
    and replacing the linked images with new ones (in this case with a private one).
    """
    db_region = db_compute_serv_with_single_image.region.single()
    db_provider = db_region.provider.single()
    db_image = db_compute_serv_with_single_image.images.single()
    item_in = create_random_compute_service(
        with_images=True, projects=[i.uuid for i in db_provider.projects]
    )
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_image,
        obj_in=item_in,
        projects=db_provider.projects,
        force=True,
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert len(item.images) == 1
    assert item.images.single() != db_image
    assert len(item.images.single().projects) > 0


def test_force_update_without_changing_images(
    db_compute_serv_with_single_image: ComputeService,
) -> None:
    """Update the attributes and relationships of an existing Compute Service.

    Update a Compute Service with a set of linked images, changing only its attributes
    leaving untouched its connections (this is different from the previous test because
    the flag force is set to True).
    """
    db_region = db_compute_serv_with_single_image.region.single()
    db_image = db_compute_serv_with_single_image.images.single()
    item_in = create_random_compute_service(with_images=True)
    for k in item_in.images[0].dict(exclude={"projects"}).keys():
        item_in.images[0].__setattr__(k, db_image.__getattribute__(k))
    item = compute_service.update(
        db_obj=db_compute_serv_with_single_image, obj_in=item_in, force=True
    )
    validate_create_compute_service_attrs(obj_in=item_in, db_item=item)
    assert item.region.single() == db_region
    assert item.images.single() == db_image


def test_delete_item(db_compute_serv: ComputeService) -> None:
    """Delete an existing Compute Service."""
    db_region = db_compute_serv.region.single()
    assert compute_service.remove(db_obj=db_compute_serv)
    assert not compute_service.get(uid=db_compute_serv.uid)
    assert region.get_multi(uid=db_region.uid)


def test_delete_item_with_flavors(
    db_compute_serv_with_single_flavor: ComputeService,
) -> None:
    """Delete an existing Compute Service and its linked flavors, images and flavors."""
    db_region = db_compute_serv_with_single_flavor.region.single()
    db_flavor = db_compute_serv_with_single_flavor.flavors.single()
    assert compute_service.remove(db_obj=db_compute_serv_with_single_flavor)
    assert not compute_service.get(uid=db_compute_serv_with_single_flavor.uid)
    assert region.get(uid=db_region.uid)
    assert not flavor.get(uid=db_flavor.uid)


def test_delete_item_with_images(
    db_compute_serv_with_single_image: ComputeService,
) -> None:
    """Delete an existing Compute Service and its linked flavors, images and images."""
    db_region = db_compute_serv_with_single_image.region.single()
    db_image = db_compute_serv_with_single_image.images.single()
    assert compute_service.remove(db_obj=db_compute_serv_with_single_image)
    assert not compute_service.get(uid=db_compute_serv_with_single_image.uid)
    assert region.get(uid=db_region.uid)
    assert not image.get(uid=db_image.uid)


def test_delete_item_with_quotas(
    db_compute_serv_with_single_quota: ComputeService,
) -> None:
    """Delete an existing Compute Service and its linked flavors, images and quotas."""
    db_region = db_compute_serv_with_single_quota.region.single()
    db_quota = db_compute_serv_with_single_quota.quotas.single()
    assert compute_service.remove(db_obj=db_compute_serv_with_single_quota)
    assert not compute_service.get(uid=db_compute_serv_with_single_quota.uid)
    assert region.get(uid=db_region.uid)
    assert not compute_quota.get(uid=db_quota.uid)
