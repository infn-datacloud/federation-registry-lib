import pytest
from app.project.models import Project
from app.quota.crud import block_storage_quota
from app.quota.models import BlockStorageQuota
from app.service.models import BlockStorageService
from tests.utils.block_storage_quota import create_random_block_storage_quota


@pytest.fixture
def db_block_storage_quota(
    db_block_storage_serv2: BlockStorageService,
) -> BlockStorageQuota:
    """Block Storage Quota of the BS Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the first project. Quota to apply to the whole user group.
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
def db_block_storage_quota_per_user(
    db_block_storage_quota: BlockStorageQuota,
) -> BlockStorageQuota:
    """Block Storage Quota of the BS Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the first project. Quota to apply to each user of the user group.
    This is currently the second quota on the same project and same service.
    """
    db_service = db_block_storage_quota.service.single()
    db_project = db_block_storage_quota.project.single()
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = True
    item = block_storage_quota.create(
        obj_in=item_in, service=db_service, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_quota2(
    db_block_storage_quota_per_user: BlockStorageQuota,
) -> BlockStorageQuota:
    """Block Storage Quota of the BS Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the second project. Quota to apply to the whole user group. This is
    the third quota on the same service.
    """
    db_service = db_block_storage_quota_per_user.service.single()
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
def db_block_storage_quota3(
    db_block_storage_quota2: BlockStorageQuota,
    db_block_storage_serv3: BlockStorageService,
) -> BlockStorageQuota:
    """Block Storage Quota of the BS Service belonging to the second region of the
    provider with a multiple projects.

    Quota points to the second project. Quota to apply to the whole user group.
    """
    db_region = db_block_storage_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_block_storage_quota(project=db_project.uuid)
    item_in.per_user = False
    item = block_storage_quota.create(
        obj_in=item_in, service=db_block_storage_serv3, project=db_project
    )
    yield item


@pytest.fixture
def db_block_storage_serv_with_single_quota(
    db_block_storage_quota: BlockStorageQuota,
) -> BlockStorageService:
    """Project with single Block Storage Quota."""
    yield db_block_storage_quota.service.single()


@pytest.fixture
def db_block_storage_serv_with_multiple_quotas_same_project(
    db_block_storage_quota_per_user: BlockStorageQuota,
) -> BlockStorageService:
    """Project with multiple Block Storage Quota on same project."""
    yield db_block_storage_quota_per_user.service.single()


@pytest.fixture
def db_block_storage_serv_with_multiple_quotas(
    db_block_storage_quota2: BlockStorageQuota,
) -> BlockStorageService:
    """Project with multiple Block Storage Quota on multiple projects."""
    yield db_block_storage_quota2.service.single()


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
    db_block_storage_quota3: BlockStorageQuota,
) -> Project:
    """Project with single Block Storage Quota."""
    yield db_block_storage_quota3.project.single()
