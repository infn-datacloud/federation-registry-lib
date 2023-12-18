"""BlockStorageService specific fixtures."""
from pytest_cases import fixture, fixture_union, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import BlockStorageServiceCreateExtended
from app.region.models import Region
from app.service.crud import block_storage_service_mng
from app.service.models import BlockStorageService
from tests.quotas.block_storage_quota.utils import (
    random_block_storage_quota_required_attr,
)
from tests.services.block_storage_service.utils import (
    random_block_storage_service_required_attr,
)


@fixture
def db_block_storage_service_simple(db_region_simple: Region) -> BlockStorageService:
    """Fixture with standard DB BlockStorageService."""
    item = random_block_storage_service_required_attr()
    return block_storage_service_mng.create(
        obj_in=BlockStorageServiceCreateExtended(**item), region=db_region_simple
    )


@fixture
def db_block_storage_service_with_single_project(
    db_region_with_single_project: Region,
) -> BlockStorageService:
    """Fixture with standard DB BlockStorageService."""
    item = random_block_storage_service_required_attr()
    return block_storage_service_mng.create(
        obj_in=BlockStorageServiceCreateExtended(**item),
        region=db_region_with_single_project,
    )


@fixture
@parametrize(owned_quotas=[1, 2])
def db_block_storage_service_with_quotas(
    owned_quotas: int, db_region_with_projects: Region
) -> BlockStorageService:
    """Fixture with standard DB BlockStorageService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    quotas = []
    for project_uuid in projects:
        for i in range(owned_quotas):
            quotas.append(
                {
                    **random_block_storage_quota_required_attr(),
                    "per_user": i % 2,
                    "project": project_uuid,
                }
            )
    item = {**random_block_storage_service_required_attr(), "quotas": quotas}
    return block_storage_service_mng.create(
        obj_in=BlockStorageServiceCreateExtended(**item),
        region=db_region_with_projects,
        projects=db_provider.projects,
    )


db_block_storage_service = fixture_union(
    "db_block_storage_service",
    (db_block_storage_service_simple, db_block_storage_service_with_quotas),
    idstyle="explicit",
)
