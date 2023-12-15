"""IdentityService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture

from app.provider.schemas_extended import IdentityServiceCreate
from app.region.models import Region
from app.service.crud import identity_service_mng
from app.service.models import IdentityService


@fixture
def db_identity_service(
    identity_service_create_mandatory_data: Dict[str, Any], db_region_simple: Region
) -> IdentityService:
    """Fixture with standard DB IdentityService."""
    item = IdentityServiceCreate(**identity_service_create_mandatory_data)
    return identity_service_mng.create(obj_in=item, region=db_region_simple)
