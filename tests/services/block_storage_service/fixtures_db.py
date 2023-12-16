"""BlockStorageService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    BlockStorageServiceCreateExtended,
)
from app.region.models import Region
from app.service.crud import block_storage_service_mng
from app.service.models import BlockStorageService

relationships_num = [1, 2]


@fixture
def db_block_storage_service_simple(
    block_storage_service_create_mandatory_data: Dict[str, Any],
    db_region_simple: Region,
) -> BlockStorageService:
    """Fixture with standard DB BlockStorageService."""
    item = BlockStorageServiceCreateExtended(
        **block_storage_service_create_mandatory_data
    )
    return block_storage_service_mng.create(obj_in=item, region=db_region_simple)


@fixture
def db_block_storage_service_with_single_project(
    block_storage_service_create_mandatory_data: Dict[str, Any],
    db_region_with_single_project: Region,
) -> BlockStorageService:
    """Fixture with standard DB BlockStorageService."""
    item = BlockStorageServiceCreateExtended(
        **block_storage_service_create_mandatory_data
    )
    return block_storage_service_mng.create(
        obj_in=item, region=db_region_with_single_project
    )


@fixture
@parametrize(owned_quotas=relationships_num)
def db_block_storage_service_with_quotas(
    owned_quotas: int,
    block_storage_service_create_mandatory_data: Dict[str, Any],
    db_region_with_projects: Region,
) -> BlockStorageService:
    """Fixture with standard DB BlockStorageService."""
    db_provider: Provider = db_region_with_projects.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    quotas = []
    for i in projects:
        for n in range(owned_quotas):
            quotas.append(BlockStorageQuotaCreateExtended(per_user=n % 2, project=i))
    item = BlockStorageServiceCreateExtended(
        **block_storage_service_create_mandatory_data, quotas=quotas
    )
    return block_storage_service_mng.create(
        obj_in=item, region=db_region_with_projects, projects=db_provider.projects
    )


db_block_storage_service = fixture_union(
    "db_block_storage_service",
    (db_block_storage_service_simple, db_block_storage_service_with_quotas),
    idstyle="explicit",
)
