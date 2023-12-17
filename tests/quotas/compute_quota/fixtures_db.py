"""ComputeQuota specific fixtures."""
from pytest_cases import fixture

from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import ComputeQuotaCreateExtended
from app.quota.crud import compute_quota_mng
from app.quota.models import ComputeQuota
from app.region.models import Region
from app.service.models import ComputeService
from tests.quotas.compute_quota.utils import random_compute_quota_required_attr


@fixture
def db_compute_quota(
    db_compute_service_with_single_project: ComputeService,
) -> ComputeQuota:
    """Fixture with standard DB ComputeQuota."""
    db_region: Region = db_compute_service_with_single_project.region.single()
    db_provider: Provider = db_region.provider.single()
    db_project: Project = db_provider.projects.single()
    item = ComputeQuotaCreateExtended(
        **random_compute_quota_required_attr(), project=db_project.uuid
    )
    return compute_quota_mng.create(
        obj_in=item, service=db_compute_service_with_single_project, project=db_project
    )
