"""BlockStorageQuota specific fixtures."""
from typing import Any, Dict

import pytest
from pytest_cases import fixture

from app.provider.models import Provider
from app.provider.schemas_extended import BlockStorageQuotaCreateExtended
from app.quota.crud import block_storage_quota_mng
from app.quota.models import BlockStorageQuota
from app.region.models import Region
from app.service.models import BlockStorageService


@fixture
def db_block_storage_quota(
    block_storage_quota_create_mandatory_data: Dict[str, Any],
    db_block_storage_service_with_projects: BlockStorageService,
) -> BlockStorageQuota:
    """Fixture with standard DB BlockStorageQuota."""
    db_region: Region = db_block_storage_service_with_projects.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    if len(projects) > 1:
        pytest.skip("Case with multiple projects are ignored.")

    item = BlockStorageQuotaCreateExtended(
        **block_storage_quota_create_mandatory_data, project=projects[0]
    )
    return block_storage_quota_mng.create(
        obj_in=item,
        service=db_block_storage_service_with_projects,
        project=db_provider.projects.single(),
    )
