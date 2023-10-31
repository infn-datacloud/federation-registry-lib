import pytest
from app.flavor.models import Flavor
from app.image.crud import image
from app.image.models import Image
from app.project.models import Project
from app.service.models import ComputeService
from tests.utils.image import create_random_image


@pytest.fixture
def db_public_image(db_compute_serv2: ComputeService) -> Image:
    """Public image of a compute service."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv2)
    yield item


@pytest.fixture
def db_private_image(db_public_image: Image) -> Image:
    """First private image of a compute service.

    It belongs to a specific project. It's the second image on the same
    service.
    """
    db_service = db_public_image.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_image(projects=[db_project.uuid])
    item = image.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_image_multiple_projects(db_public_image: Image) -> Image:
    """First private image of a compute service.

    It belongs to a all projects. It's the second image on the same
    service.
    """
    db_service = db_public_image.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_image(projects=[i.uuid for i in db_provider.projects])
    item = image.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_image2(db_private_image: Image) -> Image:
    """Second private image of a compute service.

    It belongs to a specific project. It's the third image on the same
    service.
    """
    db_service = db_private_image.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_image(projects=[db_project.uuid])
    item = image.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_image3(
    db_private_image2: Image, db_compute_serv3: ComputeService
) -> Image:
    """First private image of another compute service.

    It belongs to a specific project. It's the first image on a
    different service.
    """
    db_region = db_compute_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_image(projects=[db_project.uuid])
    item = image.create(
        obj_in=item_in, service=db_compute_serv3, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_shared_image(db_compute_serv2: ComputeService, db_compute_serv3) -> Flavor:
    """Public image shared between different compute services of the same
    provider."""
    item_in = create_random_image()
    item = image.create(obj_in=item_in, service=db_compute_serv2)
    item = image.create(obj_in=item_in, service=db_compute_serv3)
    yield item


@pytest.fixture
def db_compute_serv_with_single_image(db_public_image: Image) -> ComputeService:
    """Project with single Image."""
    yield db_public_image.services.all()[0]


@pytest.fixture
def db_compute_serv_with_multiple_images(db_private_image: Image) -> ComputeService:
    """Project with multiple Images (public and private ones)."""
    yield db_private_image.services.all()[0]


@pytest.fixture
def db_project_with_single_private_image(db_private_image: Image) -> Project:
    """Project with single private Image."""
    yield db_private_image.projects.all()[0]


@pytest.fixture
def db_project_with_multiple_private_images_same_service(
    db_private_image2: Image,
) -> Project:
    """Project with multiple Images on same service."""
    yield db_private_image2.projects.all()[0]


@pytest.fixture
def db_project_with_multiple_private_images_diff_service(
    db_private_image3: Image,
) -> Project:
    """Project with multiple Images on different services."""
    yield db_private_image3.projects.all()[0]
