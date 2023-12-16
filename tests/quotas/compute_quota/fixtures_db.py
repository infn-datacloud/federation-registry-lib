"""ComputeQuota specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture

from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import ComputeQuotaCreateExtended
from app.quota.crud import compute_quota_mng
from app.quota.models import ComputeQuota
from app.region.models import Region
from app.service.models import ComputeService


@fixture
def db_compute_quota(
    compute_quota_create_mandatory_data: Dict[str, Any],
    db_compute_service_with_single_project: ComputeService,
) -> ComputeQuota:
    """Fixture with standard DB ComputeQuota."""
    db_region: Region = db_compute_service_with_single_project.region.single()
    db_provider: Provider = db_region.provider.single()
    db_project: Project = db_provider.projects.single()
    item = ComputeQuotaCreateExtended(
        **compute_quota_create_mandatory_data, project=db_project.uuid
    )
    return compute_quota_mng.create(
        obj_in=item, service=db_compute_service_with_single_project, project=db_project
    )
