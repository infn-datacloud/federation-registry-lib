"""ComputeQuota specific fixtures."""
from typing import Any, Dict

import pytest
from pytest_cases import fixture

from app.provider.models import Provider
from app.provider.schemas_extended import ComputeQuotaCreateExtended
from app.quota.crud import compute_quota_mng
from app.quota.models import ComputeQuota
from app.region.models import Region
from app.service.models import ComputeService


@fixture
def db_compute_quota(
    compute_quota_create_mandatory_data: Dict[str, Any],
    db_compute_service_with_projects: ComputeService,
) -> ComputeQuota:
    """Fixture with standard DB ComputeQuota."""
    db_region: Region = db_compute_service_with_projects.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    if len(projects) > 1:
        pytest.skip("Case with multiple projects are ignored.")

    item = ComputeQuotaCreateExtended(
        **compute_quota_create_mandatory_data, project=projects[0]
    )
    return compute_quota_mng.create(
        obj_in=item,
        service=db_compute_service_with_projects,
        project=db_provider.projects.single(),
    )
