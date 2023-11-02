import pytest
from app.region.models import Region
from app.service.crud import identity_service
from app.service.models import IdentityService
from tests.utils.identity_service import create_random_identity_service


@pytest.fixture
def db_identity_serv(db_region: Region) -> IdentityService:
    """Identity service on the region of the first provider."""
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region)
    yield item


@pytest.fixture
def db_identity_serv2(db_region3: Region) -> IdentityService:
    """Identity service on second region of the second provider."""
    item_in = create_random_identity_service()
    item = identity_service.create(obj_in=item_in, region=db_region3)
    yield item


@pytest.fixture
def db_region_with_identity_service(db_identity_serv: IdentityService) -> Region:
    """Region with a identity service."""
    yield db_identity_serv.region.single()


@pytest.fixture
def db_deletable_region_with_identity_service(
    db_identity_serv2: IdentityService,
) -> Region:
    """Region with a identity service.

    Region can be deleted.
    """
    yield db_identity_serv2.region.single()
