import pytest

from app.project.models import Project
from app.quota.crud import compute_quota
from app.quota.models import ComputeQuota
from app.service.models import ComputeService
from tests.utils.compute_quota import create_random_compute_quota


@pytest.fixture
def db_compute_quota(db_compute_serv: ComputeService) -> ComputeQuota:
    """First Compute Quota.

    It belongs to the Compute Service belonging to the region of the provider
    with a single project.
    Quota points to the provider's unique project. Quota to apply to the whole user
    group.
    """
    db_region = db_compute_serv.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_quota2(db_compute_serv2: ComputeService) -> ComputeQuota:
    """Second Compute Quota.

    It belongs to the Compute Service belonging to the first region of the
    provider with multiple projects.
    Quota points to the provider's first project. Quota to apply to the whole user
    group.
    """
    db_region = db_compute_serv2.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv2, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_quota3(db_compute_serv3: ComputeService) -> ComputeQuota:
    """Third Compute Quota.

    It belongs to the Compute Service belonging to the second region of the
    provider with multiple projects.
    Quota points to the provider's first project. Quota to apply to the whole user
    group.
    """
    db_region = db_compute_serv3.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(
        obj_in=item_in, service=db_compute_serv3, project=db_project
    )
    yield item


@pytest.fixture
def db_compute_quota_per_user(db_compute_quota3: ComputeQuota) -> ComputeQuota:
    """Compute Quota with limitations to apply to single users.

    It belongs to the Compute Service belonging to the second region of the
    provider with multiple projects.
    Quota points to the provider's first project. Quota to apply to each user.
    """
    db_service = db_compute_quota3.service.single()
    db_project = db_compute_quota3.project.single()
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = True
    item = compute_quota.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_compute_quota4(db_compute_quota3: ComputeQuota) -> ComputeQuota:
    """Second Compute Quota on Compute service of the second region of the
    provider with multiple projects.

    Quota points to the provider's second project. Quota to apply to the whole user
    group.
    """
    db_service = db_compute_quota3.service.single()
    db_region = db_service.region.single()
    db_provider = db_region.provider.single()
    db_project = db_provider.projects.all()[1]
    item_in = create_random_compute_quota(project=db_project.uuid)
    item_in.per_user = False
    item = compute_quota.create(obj_in=item_in, service=db_service, project=db_project)
    yield item


@pytest.fixture
def db_compute_serv_with_single_quota(
    db_compute_quota: ComputeQuota,
) -> ComputeService:
    """Service with single Compute Quota."""
    yield db_compute_quota.service.single()


@pytest.fixture
def db_compute_serv_with_multiple_quotas_same_project(
    db_compute_quota_per_user: ComputeQuota,
) -> ComputeService:
    """Service with multiple Compute Quota on same project."""
    yield db_compute_quota_per_user.service.single()


@pytest.fixture
def db_compute_serv_with_multiple_quotas(
    db_compute_quota4: ComputeQuota,
) -> ComputeService:
    """Service with multiple Compute Quota on multiple projects."""
    yield db_compute_quota4.service.single()


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
    db_compute_quota2: ComputeQuota, db_compute_quota3: ComputeQuota
) -> Project:
    """Project with single Compute Quota."""
    yield db_compute_quota3.project.single()
