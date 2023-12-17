"""IdentityService specific fixtures."""
from pytest_cases import fixture

from app.provider.schemas_extended import IdentityServiceCreate
from app.region.models import Region
from app.service.crud import identity_service_mng
from app.service.models import IdentityService
from tests.services.identity_service.utils import random_identity_service_required_attr


@fixture
def db_identity_service(db_region_simple: Region) -> IdentityService:
    """Fixture with standard DB IdentityService."""
    item = IdentityServiceCreate(**random_identity_service_required_attr())
    return identity_service_mng.create(obj_in=item, region=db_region_simple)
