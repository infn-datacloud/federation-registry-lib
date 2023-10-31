from uuid import uuid4

from app.image.crud import image
from app.image.models import Image
from app.project.crud import project
from app.service.models import ComputeService
from tests.utils.image import (
    create_random_image,
    create_random_image_patch,
    validate_create_image_attrs,
)
from tests.utils.project import create_random_project


def test_create_item(db_compute_serv: ComputeService) -> None:
    """Create an Image belonging to a specific Compute Service."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv)
    validate_create_image_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(db_compute_serv: ComputeService) -> None:
    """Create an Image, with default values when possible, belonging to a
    specific Compute Service."""
    item_in = create_random_image(default=True)
    item = image.create(obj_in=item_in, service=db_compute_serv)
    validate_create_image_attrs(obj_in=item_in, db_item=item)


def test_create_item_private(db_compute_serv: ComputeService) -> None:
    """Create a private Image belonging to a specific Compute Service.

    Private Images requires a list of allowed projects.
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_image(projects=[i.uuid for i in db_provider.projects])
    item = image.create(
        obj_in=item_in, service=db_compute_serv, projects=db_provider.projects
    )
    validate_create_image_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_same_uuid_diff_provider(
    db_compute_serv: ComputeService, db_compute_serv2: ComputeService
) -> None:
    """Create a public Image belonging to a specific Compute Service.

    Connect a Image with the same UUID to another Provider. This
    operation is allowed since the images belong to different providers.
    """
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv)
    validate_create_image_attrs(obj_in=item_in, db_item=item)
    item2 = image.create(obj_in=item_in, service=db_compute_serv2)
    validate_create_image_attrs(obj_in=item_in, db_item=item)
    assert item.uid != item2.uid


def test_connect_same_item_to_different_service(
    db_compute_serv2: ComputeService, db_compute_serv3: ComputeService
) -> None:
    """Create a public Image belonging to a specific Compute Service.

    Connect this same Image to another Compute Service of the same
    Provider. This operation is performed creating again the same image
    but passing another service.
    """
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv2)
    validate_create_image_attrs(obj_in=item_in, db_item=item)
    item2 = image.create(obj_in=item_in, service=db_compute_serv3)
    validate_create_image_attrs(obj_in=item_in, db_item=item)
    assert item.uid == item2.uid


def test_get_item(db_private_image: Image) -> None:
    """Retrieve an Image from its UID."""
    item = image.get(uid=db_private_image.uid)
    assert item.uid == db_private_image.uid


def test_get_non_existing_item() -> None:
    """Try to retrieve a not existing Image."""
    assert not image.get(uid=uuid4())


def test_get_items(db_compute_serv: ComputeService) -> None:
    """Retrieve multiple images."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv)
    item_in2 = create_random_image()
    item2 = image.create(obj_in=item_in2, service=db_compute_serv)

    stored_items = image.get_multi()
    assert len(stored_items) == 2

    stored_items = image.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_create_image_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = image.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_create_image_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(db_compute_serv: ComputeService) -> None:
    """Test the 'limit' attribute in GET operations."""
    item_in = create_random_image()
    image.create(obj_in=item_in, service=db_compute_serv)
    item_in2 = create_random_image()
    image.create(obj_in=item_in2, service=db_compute_serv)

    stored_items = image.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = image.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = image.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(db_compute_serv: ComputeService) -> None:
    """Test the 'sort' attribute in GET operations."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv)
    item_in2 = create_random_image()
    item2 = image.create(obj_in=item_in2, service=db_compute_serv)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = image.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = image.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(db_compute_serv: ComputeService) -> None:
    """Test the 'skip' attribute in GET operations."""
    item_in = create_random_image()
    image.create(obj_in=item_in, service=db_compute_serv)
    item_in2 = create_random_image()
    image.create(obj_in=item_in2, service=db_compute_serv)

    stored_items = image.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = image.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(db_compute_serv: ComputeService) -> None:
    """Update the attributes of an existing Image, without updating its
    relationships."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv)
    patch_in = create_random_image_patch()
    patch_in.is_public = item.is_public
    item = image.update(db_obj=item, obj_in=patch_in)
    for k, v in patch_in.dict().items():
        item_in.__setattr__(k, v)
    validate_create_image_attrs(obj_in=item_in, db_item=item)


def test_patch_item_with_defaults(db_compute_serv: ComputeService) -> None:
    """Try to update the attributes of an existing Image, without updating its
    relationships, with default values.

    The first attempt fails (no updates); the second one, with explicit
    default values, succeeds.
    """
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv)
    patch_in = create_random_image_patch(default=True)
    assert not image.update(db_obj=item, obj_in=patch_in)

    patch_in = create_random_image_patch(default=True)
    patch_in.description = ""
    patch_in.is_public = item.is_public
    item = image.update(db_obj=item, obj_in=patch_in)
    item_in.description = patch_in.description
    validate_create_image_attrs(obj_in=item_in, db_item=item)


# TODO try to patch image setting it as private when there are no projects
# or public when it has related projects


def test_forced_update_item(db_compute_serv: ComputeService) -> None:
    """Update the attributes and relationships of an existing Image.

    At first update a Image with a set of linked projects, updating its
    attributes and removing all linked projects.

    Update a Image with no projects, changing its attributes and linking
    a new project.

    Update a Image with a set of linked projects, changing both its
    attributes and replacing the linked projects with new ones.

    Update a Image with a set of linked projects, changing only its
    attributes leaving untouched its connections (this is different from
    the previous test because the flag force is set to True).
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    project1 = db_provider.projects.single()
    item_in = create_random_image(projects=[project1.uuid])
    item = image.create(
        obj_in=item_in, service=db_compute_serv, projects=db_provider.projects
    )
    item_in = create_random_image()
    item = image.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_image_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_image(projects=[project1.uuid])
    item = image.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_image_attrs(obj_in=item_in, db_item=item)

    project2 = project.create(obj_in=create_random_project(), provider=db_provider)
    item_in = create_random_image(projects=[project2.uuid])
    item = image.update(
        db_obj=item, obj_in=item_in, projects=db_provider.projects, force=True
    )
    validate_create_image_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_image(projects=item_in.projects)
    item = image.update(db_obj=item, obj_in=item_in, force=True)
    validate_create_image_attrs(obj_in=item_in, db_item=item)


def test_delete_item(db_compute_serv: ComputeService) -> None:
    """Delete an existing public Image."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv)
    result = image.remove(db_obj=item)
    assert result
    item = image.get(uid=item.uid)
    assert not item
    assert db_compute_serv


def test_delete_item_with_relationships(db_compute_serv: ComputeService) -> None:
    """Delete an existing private Image.

    Do not delete linked projects
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_image(projects=[i.uuid for i in db_provider.projects])
    item = image.create(
        obj_in=item_in, service=db_compute_serv, projects=db_provider.projects
    )
    num_db_project = len(db_provider.projects)
    result = image.remove(db_obj=item)
    assert result
    item = image.get(uid=item.uid)
    assert not item
    assert len(db_provider.projects) == num_db_project
