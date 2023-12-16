"""BlockStorageQuota specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture

from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import BlockStorageQuotaCreateExtended
from app.quota.crud import block_storage_quota_mng
from app.quota.models import BlockStorageQuota
from app.region.models import Region
from app.service.models import BlockStorageService


@fixture
def db_block_storage_quota(
    block_storage_quota_create_mandatory_data: Dict[str, Any],
    db_block_storage_service_with_single_project: BlockStorageService,
) -> BlockStorageQuota:
    """Fixture with standard DB BlockStorageQuota."""
    db_region: Region = db_block_storage_service_with_single_project.region.single()
    db_provider: Provider = db_region.provider.single()
    db_project: Project = db_provider.projects.single()
    item = BlockStorageQuotaCreateExtended(
        **block_storage_quota_create_mandatory_data, project=db_project.uuid
    )
    return block_storage_quota_mng.create(
        obj_in=item,
        service=db_block_storage_service_with_single_project,
        project=db_project,
    )
