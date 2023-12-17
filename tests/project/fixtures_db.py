"""Project specific fixtures."""
from typing import Union

import pytest
from pytest_cases import fixture, fixture_ref, fixture_union, parametrize

from app.flavor.models import Flavor
from app.image.models import Image
from app.network.models import Network
from app.project.models import Project
from app.provider.models import Provider
from app.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota


@fixture
@parametrize(
    db_provider=[
        fixture_ref("db_provider_with_single_project"),
        fixture_ref("db_provider_with_idps"),
    ]
)
def db_project_from_provider(db_provider: Provider) -> Project:
    """Fixture with standard DB Project."""
    return db_provider.projects.single()


@fixture
@parametrize(
    db_quota=[
        fixture_ref("db_block_storage_quota"),
        fixture_ref("db_compute_quota"),
        fixture_ref("db_network_quota"),
    ]
)
def db_project_from_quota(
    db_quota: Union[BlockStorageQuota, ComputeQuota, NetworkQuota],
) -> Project:
    """Fixture with standard DB Project."""
    return db_quota.project.single()


@fixture
@parametrize(
    db_resource=[fixture_ref("db_flavor_simple"), fixture_ref("db_image_simple")]
)
def db_project_from_compute_resource(db_resource: Union[Flavor, Image]) -> Project:
    """Fixture with standard DB Project."""
    if db_resource.is_public:
        pytest.skip("Case with public flavor or image does not have a project.")
    return db_resource.projects.single()


@fixture
def db_project_from_network_resource(db_network: Network) -> Project:
    """Fixture with standard DB Project."""
    if db_network.is_shared:
        pytest.skip("Case with shared network does not have a project.")
    return db_network.project.single()


db_project = fixture_union(
    "db_project",
    (
        db_project_from_provider,
        db_project_from_quota,
        db_project_from_compute_resource,
        db_project_from_network_resource,
    ),
    idstyle="explicit",
)
