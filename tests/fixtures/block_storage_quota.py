import pytest

from app.project.models import Project
from app.quota.crud import block_storage_quota
from app.quota.models import BlockStorageQuota
from app.service.models import BlockStorageService
from tests.utils.block_storage_quota import create_random_block_storage_quota


@pytest.fixture
def db_block_storage_quota(
    db_block_storage_serv: BlockStorageService
) -> BlockStorageQuota:
    """First Block Storage Quota.

    It belongs to the Block Storage Service belonging to the region of the provider
    with a single project.
    Quota points to the provider's unique project. Quota to apply to the whole user
    group.
    """
    db_region = db_block_storage_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota2(
    db_block_storage_serv2: BlockStorageService
) -> BlockStorageQuota:
    """Second Block Storage Quota.

    It belongs to the Block Storage Service belonging to the first region of the
    provider with multiple projects.
    Quota points to the provider's first project. Quota to apply to the whole user
    group.
    """
    db_region = db_block_storage_serv2.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv2, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota3(
    db_block_storage_serv3: BlockStorageService
) -> BlockStorageQuota:
    """Third Block Storage Quota.

    It belongs to the Block Storage Service belonging to the second region of the
    provider with multiple projects.
    Quota points to the provider's first project. Quota to apply to the whole user
    group.
    """
    db_region = db_block_storage_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv3, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota_per_user(
    db_block_storage_quota3: BlockStorageQuota
) -> BlockStorageQuota:
    """Block Storage Quota with limitations to apply to single users.

    It belongs to the Block Storage Service belonging to the second region of the
    provider with multiple projects.
    Quota points to the provider's first project. Quota to apply to each user.
    """
    db_service = db_block_storage_quota3.service.single()
    db_project = db_block_storage_quota3.project.single()
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = True
    item = block_storage_quota.create(
        obj_in=item_in, service=db_service, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota4(
    db_block_storage_quota3: BlockStorageQuota
) -> BlockStorageQuota:
    """Second Block Storage Quota on Block Storage service of the second region of the
    provider with multiple projects.

    Quota points to the provider's second project. Quota to apply to the whole user
    group.
    """
    db_service = db_block_storage_quota3.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_service, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_serv_with_single_quota(
    db_block_storage_quota: BlockStorageQuota,
) -> BlockStorageService:
    """Service with single Block Storage Quota."""
    yield db_block_storage_quota.service.single()


@pytest.fixture
def db_block_storage_serv_with_multiple_quotas_same_project(
    db_block_storage_quota_per_user: BlockStorageQuota,
) -> BlockStorageService:
    """Service with multiple Block Storage Quota on same project."""
    yield db_block_storage_quota_per_user.service.single()


@pytest.fixture
def db_block_storage_serv_with_multiple_quotas(
    db_block_storage_quota4: BlockStorageQuota,
) -> BlockStorageService:
    """Service with multiple Block Storage Quota on multiple projects."""
    yield db_block_storage_quota4.service.single()


@pytest.fixture
def db_project_with_single_block_storage_quota(
    db_block_storage_quota: BlockStorageQuota,
) -> Project:
    """Project with single Block Storage Quota."""
    yield db_block_storage_quota.project.single()


@pytest.fixture
def db_project_with_multiple_block_storage_quotas_same_service(
    db_block_storage_quota_per_user: BlockStorageQuota,
) -> Project:
    """Project with multiple Block Storage Quotas on same service."""
    yield db_block_storage_quota_per_user.project.single()


@pytest.fixture
def db_project_with_multiple_block_storage_quotas_diff_service(
    db_block_storage_quota2: BlockStorageQuota,
    db_block_storage_quota3: BlockStorageQuota,
) -> Project:
    """Project with single Block Storage Quota."""
    yield db_block_storage_quota3.project.single()
