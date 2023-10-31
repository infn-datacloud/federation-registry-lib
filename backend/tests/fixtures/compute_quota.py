import pytest
from app.project.models import Project
from app.quota.crud import compute_quota
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.service.models import BlockStorageService, ComputeService
from tests.utils.compute_quota import create_random_compute_quota


@pytest.fixture
def db_compute_quota(
    db_compute_serv2: BlockStorageService,
) -> BlockStorageQuota:
    """Compute Quota of the C Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the first project. Quota to apply to the whole user
    group.
    """
    db_region = db_compute_serv2.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv2, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_quota_per_user(
    db_compute_quota: ComputeQuota,
) -> ComputeQuota:
    """Compute Quota of the C Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the first project. Quota to apply to each user of
    the user group. This is currently the second quota on the same
    project and same service.
    """
    db_service = db_compute_quota.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[0]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = True
    item = compute_quota.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_compute_quota2(
    db_compute_quota_per_user: ComputeQuota,
) -> ComputeQuota:
    """Compute Quota of the C Service belonging to the first region of the
    provider with multiple projects.

    Quota points to the second project. Quota to apply to the whole user
    group. This is the third quota on the same service.
    """
    db_service = db_compute_quota_per_user.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_compute_quota3(
    db_compute_quota2: ComputeQuota,
    db_compute_serv3: ComputeService,
) -> ComputeQuota:
    """Compute Quota of the C Service belonging to the second region of the
    provider with a multiple projects.

    Quota points to the second project. Quota to apply to the whole user
    group.
    """
    db_region = db_compute_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv3, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_serv_with_single_quota(
    db_compute_quota: ComputeQuota,
) -> ComputeService:
    """Project with single Compute Quota."""
    yield db_compute_quota.service.all()[0]


@pytest.fixture
def db_compute_serv_with_multiple_quotas(
    db_compute_quota2: ComputeQuota,
) -> ComputeService:
    """Project with single Compute Quota."""
    yield db_compute_quota2.service.all()[0]


@pytest.fixture
def db_project_with_single_compute_quota(
    db_compute_quota: ComputeQuota,
) -> Project:
    """Project with single Compute Quota."""
    yield db_compute_quota.project.single()


@pytest.fixture
def db_project_with_multiple_compute_quotas_same_service(
    db_compute_quota_per_user: ComputeQuota,
) -> Project:
    """Project with multiple Compute Quotas on same service."""
    yield db_compute_quota_per_user.project.single()


@pytest.fixture
def db_project_with_multiple_compute_quotas_diff_service(
    db_compute_quota3: ComputeQuota,
) -> Project:
    """Project with multiple Compute Quotas on different services."""
    yield db_compute_quota3.project.single()
