import pytest
from app.region.models import Region
from app.service.crud import compute_service
from app.service.models import ComputeService
from tests.utils.compute_service import create_random_compute_service


@pytest.fixture
def db_compute_serv(db_region: Region) -> ComputeService:
    """Compute service on the region of the first provider."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_compute_serv2(db_region2: Region) -> ComputeService:
    """Compute service on first region of the second provider."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_compute_serv3(db_region3: Region) -> ComputeService:
    """Compute service on the second region of the second provider."""
    item_in = create_random_compute_service()
    item = compute_service.create(obj_in=item_in, region=db_region3)
    yield item


# TODO Add fixture of second compute_service for the same region?


@pytest.fixture
def db_region_with_compute_service(db_compute_serv: ComputeService) -> Region:
    """Region with a block storage service."""
    yield db_compute_serv.region.single()


@pytest.fixture
def db_deletable_region_with_compute_service(
    db_compute_serv3: ComputeService,
) -> Region:
    """Region with a block storage service."""
    yield db_compute_serv3.region.single()


# TODO Add fixture of region with multiple compute_services?
