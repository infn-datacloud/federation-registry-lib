import pytest
from app.network.crud import network
from app.network.models import Network
from app.project.models import Project
from app.service.models import NetworkService
from tests.utils.network import create_random_network

# NETWORKS (and related services and projects)


@pytest.fixture
def db_public_network(db_network_serv2: NetworkService) -> Network:
    """Public network of a network service."""
    item_in = create_random_network()
    item = network.create(obj_in=item_in, service=db_network_serv2)
    yield item


@pytest.fixture
def db_private_network(db_public_network: Network) -> Network:
    """First private network of a network service.

    It belongs to a specific project. It's the second network on the
    same service.
    """
    db_service = db_public_network.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_network(project=db_project.uuid)
    item = network.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_private_network2(db_private_network: Network) -> Network:
    """Second private network of a network service.

    It belongs to a specific project. It's the third network on the same
    service.
    """
    db_service = db_private_network.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_network(project=db_project.uuid)
    item = network.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_private_network3(
    db_private_network2: Network, db_network_serv3: NetworkService
) -> Network:
    """First private network of another network service.

    It belongs to a specific project. It's the first network on a
    different service.
    """
    db_region = db_network_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_network(project=db_project.uuid)
    item = network.create(obj_in=item_in, service=db_network_serv3, project=db_project)
    yield item


@pytest.fixture
def db_network_serv_with_single_network(db_public_network: Network) -> NetworkService:
    """Network service with single Network."""
    yield db_public_network.service.single()


@pytest.fixture
def db_network_serv_with_multiple_networks(
    db_private_network: Network,
) -> NetworkService:
    """Network service with multiple Networks (public and private ones)."""
    yield db_private_network.service.single()


@pytest.fixture
def db_project_with_single_private_network(db_private_network: Network) -> Project:
    """Project with single private Network."""
    yield db_private_network.project.single()


@pytest.fixture
def db_project_with_multiple_private_networks_same_service(
    db_private_network2: Network,
) -> Project:
    """Project with multiple Networks on same service."""
    yield db_private_network2.project.single()


@pytest.fixture
def db_project_with_multiple_private_networks_diff_service(
    db_private_network3: Network,
) -> Project:
    """Project with multiple Networks on different services."""
    yield db_private_network3.project.single()
