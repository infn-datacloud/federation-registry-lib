"""Project specific fixtures."""
from typing import Union

from pytest_cases import fixture, fixture_ref, fixture_union, parametrize

from app.flavor.models import Flavor
from app.image.models import Image
from app.network.models import Network
from app.project.models import Project
from app.provider.models import Provider
from app.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota


@fixture
@parametrize(
    db_resource=[
        fixture_ref("db_block_storage_quota"),
        fixture_ref("db_compute_quota"),
        fixture_ref("db_network_quota"),
        fixture_ref("db_network_private"),
    ]
)
def db_project_from_item_with_single(
    db_resource: Union[BlockStorageQuota, ComputeQuota, Network, NetworkQuota],
) -> Project:
    """Fixture with standard DB Project."""
    return db_resource.project.single()


@fixture
@parametrize(
    db_resource=[
        fixture_ref("db_provider_with_single_project"),
        fixture_ref("db_flavor_single_project"),
        fixture_ref("db_image_single_project"),
    ]
)
def db_project_from_item_with_multiples(
    db_resource: Union[Provider, Flavor, Image],
) -> Project:
    """Fixture with standard DB Project."""
    return db_resource.projects.single()


db_project = fixture_union(
    "db_project",
    (db_project_from_item_with_multiples, db_project_from_item_with_single),
    idstyle="explicit",
)
