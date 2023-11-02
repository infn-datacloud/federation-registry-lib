import pytest
from app.region.models import Region
from app.service.crud import network_service
from app.service.models import NetworkService
from tests.utils.network_service import create_random_network_service


@pytest.fixture
def db_network_serv(db_region: Region) -> NetworkService:
    """Network service on the region of the first provider."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_network_serv2(db_region2: Region) -> NetworkService:
    """Network service on first region of the second provider."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_network_serv3(db_region3: Region) -> NetworkService:
    """Network service on the second region of the second provider."""
    item_in = create_random_network_service()
    item = network_service.create(obj_in=item_in, region=db_region3)
    yield item


# TODO Add fixture of second network_service for the same region?


@pytest.fixture
def db_region_with_network_service(db_network_serv: NetworkService) -> Region:
    """Region with a network service."""
    yield db_network_serv.region.single()


@pytest.fixture
def db_deletable_region_with_network_service(
    db_network_serv3: NetworkService,
) -> Region:
    """Region with a network service.

    Region can be deleted.
    """
    yield db_network_serv3.region.single()


# TODO Add fixture of region with multiple network_services?
