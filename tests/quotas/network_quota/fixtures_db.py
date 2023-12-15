"""NetworkQuota specific fixtures."""
from typing import Any, Dict

import pytest
from pytest_cases import fixture

from app.provider.models import Provider
from app.provider.schemas_extended import NetworkQuotaCreateExtended
from app.quota.crud import network_quota_mng
from app.quota.models import NetworkQuota
from app.region.models import Region
from app.service.models import NetworkService


@fixture
def db_network_quota(
    network_quota_create_mandatory_data: Dict[str, Any],
    db_network_service_with_projects: NetworkService,
) -> NetworkQuota:
    """Fixture with standard DB NetworkQuota."""
    db_region: Region = db_network_service_with_projects.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    if len(projects) > 1:
        pytest.skip("Case with multiple projects are ignored.")

    item = NetworkQuotaCreateExtended(
        **network_quota_create_mandatory_data, project=projects[0]
    )
    return network_quota_mng.create(
        obj_in=item,
        service=db_network_service_with_projects,
        project=db_provider.projects.single(),
    )
