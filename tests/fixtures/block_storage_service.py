import pytest

from app.region.models import Region
from app.service.crud import block_storage_service
from app.service.models import BlockStorageService
from tests.utils.block_storage_service import (
    create_random_block_storage_service,
)


@pytest.fixture
def db_block_storage_serv(db_region: Region) -> BlockStorageService:
    """Block Storage service on the region of the first provider."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_block_storage_serv2(db_region2: Region) -> BlockStorageService:
    """Block Storage service on the first region of the second provider."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region2)
    yield item


@pytest.fixture
def db_block_storage_serv3(db_region3: Region) -> BlockStorageService:
    """Block Storage service on the second region of the second provider."""
    item_in = create_random_block_storage_service()
    item = block_storage_service.create(obj_in=item_in, region=db_region3)
    yield item


# TODO Add fixture of second block_storage_service for the same region?


@pytest.fixture
def db_region_with_block_storage_service(
    db_block_storage_serv: BlockStorageService,
) -> Region:
    """Region with a block storage service."""
    yield db_block_storage_serv.region.single()


@pytest.fixture
def db_deletable_region_with_block_storage_service(
    db_block_storage_serv3: BlockStorageService,
) -> Region:
    """Region with a block storage service.

    Region can be deleted.
    """
    yield db_block_storage_serv3.region.single()


# TODO Add fixture of region with multiple block_storage_services?
