import pytest
from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.project.models import Project
from app.service.models import ComputeService
from tests.utils.flavor import create_random_flavor


@pytest.fixture
def db_public_flavor(db_compute_serv2: ComputeService) -> Flavor:
    """Public flavor of a compute service."""
    item_in = create_random_flavor()
    item = flavor.create(obj_in=item_in, service=db_compute_serv2)
    yield item


@pytest.fixture
def db_private_flavor(db_public_flavor: Flavor) -> Flavor:
    """First private flavor of a compute service.

    It belongs to a specific project. It's the second flavor on the same
    service.
    """
    db_service = db_public_flavor.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_flavor(projects=[db_project.uuid])
    item = flavor.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_flavor_multiple_projects(db_public_flavor: Flavor) -> Flavor:
    """First private flavor of a compute service.

    It belongs to a all projects. It's the second flavor on the same
    service.
    """
    db_service = db_public_flavor.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    item_in = create_random_flavor(projects=[i.uuid for i in db_provider.projects])
    item = flavor.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_flavor2(db_private_flavor: Flavor) -> Flavor:
    """Second private flavor of a compute service.

    It belongs to a specific project. It's the third flavor on the same
    service.
    """
    db_service = db_private_flavor.services.all()[0]
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_flavor(projects=[db_project.uuid])
    item = flavor.create(
        obj_in=item_in, service=db_service, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_private_flavor3(
    db_private_flavor2: Flavor, db_compute_serv3: ComputeService
) -> Flavor:
    """First private flavor of another compute service.

    It belongs to a specific project. It's the first flavor on a
    different service.
    """
    db_region = db_compute_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_flavor(projects=[db_project.uuid])
    item = flavor.create(
        obj_in=item_in, service=db_compute_serv3, projects=db_provider.projects
    )
    yield item


@pytest.fixture
def db_shared_flavor(db_compute_serv2: ComputeService, db_compute_serv3) -> Flavor:
    """Public flavor shared between different compute services of the same
    provider."""
    item_in = create_random_flavor()
    item = flavor.create(obj_in=item_in, service=db_compute_serv2)
    item = flavor.create(obj_in=item_in, service=db_compute_serv3)
    yield item


@pytest.fixture
def db_compute_serv_with_single_flavor(db_public_flavor: Flavor) -> ComputeService:
    """Project with single Flavor."""
    yield db_public_flavor.services.all()[0]


@pytest.fixture
def db_compute_serv_with_multiple_flavors(db_private_flavor: Flavor) -> ComputeService:
    """Project with multiple Flavors (public and private ones)."""
    yield db_private_flavor.services.all()[0]


@pytest.fixture
def db_project_with_single_private_flavor(db_private_flavor: Flavor) -> Project:
    """Project with single private Flavor."""
    yield db_private_flavor.projects.all()[0]


@pytest.fixture
def db_project_with_multiple_private_flavors_same_service(
    db_private_flavor2: Flavor,
) -> Project:
    """Project with multiple Flavors on same service."""
    yield db_private_flavor2.projects.all()[0]


@pytest.fixture
def db_project_with_multiple_private_flavors_diff_service(
    db_private_flavor3: Flavor,
) -> Project:
    """Project with multiple Flavors on different services."""
    yield db_private_flavor3.projects.all()[0]
