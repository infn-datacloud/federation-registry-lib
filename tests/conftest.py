"""File to set tests configuration parameters and common fixtures."""
import os
from typing import Any, Generator
from unittest.mock import MagicMock, PropertyMock, patch
from uuid import uuid4

import pytest

from fed_reg.flavor.models import Flavor
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.image.models import Image
from fed_reg.location.models import Location
from fed_reg.location.schemas import LocationCreate
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.project.schemas import ProjectCreate
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    BlockStorageServiceCreateExtended,
    ComputeQuotaCreateExtended,
    ComputeServiceCreateExtended,
    FlavorCreateExtended,
    IdentityProviderCreateExtended,
    ImageCreateExtended,
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
    NetworkServiceCreateExtended,
    RegionCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from fed_reg.service.schemas import IdentityServiceCreate
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup
from tests.create_dict import (
    auth_method_dict,
    block_storage_service_schema_dict,
    compute_service_schema_dict,
    flavor_model_dict,
    flavor_schema_dict,
    identity_provider_model_dict,
    identity_provider_schema_dict,
    identity_service_schema_dict,
    image_model_dict,
    image_schema_dict,
    location_model_dict,
    location_schema_dict,
    network_model_dict,
    network_schema_dict,
    network_service_schema_dict,
    project_model_dict,
    project_schema_dict,
    provider_model_dict,
    quota_model_dict,
    region_model_dict,
    region_schema_dict,
    service_model_dict,
    sla_model_dict,
    sla_schema_dict,
    user_group_model_dict,
    user_group_schema_dict,
)
from tests.db import MockDatabase


@pytest.fixture(autouse=True)
def clear_os_environment() -> None:
    """Clear the OS environment."""
    os.environ.clear()


@pytest.fixture(scope="session")
def db() -> MockDatabase:
    return MockDatabase()


@pytest.fixture(scope="session")
def db_core(db: MockDatabase) -> Generator[None, Any, None]:
    with patch("neomodel.core.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=str(db.db_version))
        mock_db.cypher_query.side_effect = db.query_call
        yield


@pytest.fixture(scope="session")
def db_match(db: MockDatabase) -> Generator[None, Any, None]:
    with patch("neomodel.match.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=str(db.db_version))
        mock_db.cypher_query.side_effect = db.query_call
        yield


@pytest.fixture(scope="session")
def db_rel_mgr(db: MockDatabase) -> Generator[None, Any, None]:
    with patch("neomodel.relationship_manager.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=str(db.db_version))

        d = {}
        cls_registry = MagicMock()
        cls_registry.__getitem__.side_effect = d.__getitem__
        cls_registry.__setitem__.side_effect = d.__setitem__
        mock_db._NODE_CLASS_REGISTRY = cls_registry

        yield


@pytest.fixture(scope="session", autouse=True)
def mock_db(
    db_core: None, db_match: None, db_rel_mgr: None
) -> Generator[None, Any, None]:
    yield


@pytest.fixture
def flavor_model() -> Flavor:
    d = flavor_model_dict()
    return Flavor(**d).save()


@pytest.fixture
def identity_provider_model() -> IdentityProvider:
    d = identity_provider_model_dict()
    return IdentityProvider(**d).save()


@pytest.fixture
def image_model() -> Image:
    d = image_model_dict()
    return Image(**d).save()


@pytest.fixture
def location_model() -> Location:
    d = location_model_dict()
    return Location(**d).save()


@pytest.fixture
def network_model() -> Network:
    d = network_model_dict()
    return Network(**d).save()


@pytest.fixture
def project_model() -> Project:
    d = project_model_dict()
    return Project(**d).save()


@pytest.fixture
def provider_model() -> Provider:
    d = provider_model_dict()
    return Provider(**d).save()


@pytest.fixture
def block_storage_quota_model() -> BlockStorageQuota:
    d = quota_model_dict()
    return BlockStorageQuota(**d).save()


@pytest.fixture
def compute_quota_model() -> ComputeQuota:
    d = quota_model_dict()
    return ComputeQuota(**d).save()


@pytest.fixture
def network_quota_model() -> NetworkQuota:
    d = quota_model_dict()
    return NetworkQuota(**d).save()


@pytest.fixture
def region_model() -> Region:
    d = region_model_dict()
    return Region(**d).save()


@pytest.fixture
def block_storage_service_model() -> BlockStorageService:
    d = service_model_dict()
    return BlockStorageService(**d).save()


@pytest.fixture
def compute_service_model() -> ComputeService:
    d = service_model_dict()
    return ComputeService(**d).save()


@pytest.fixture
def identity_service_model() -> IdentityService:
    d = service_model_dict()
    return IdentityService(**d).save()


@pytest.fixture
def network_service_model() -> NetworkService:
    d = service_model_dict()
    return NetworkService(**d).save()


@pytest.fixture
def sla_model() -> SLA:
    d = sla_model_dict()
    return SLA(**d).save()


@pytest.fixture
def user_group_model() -> UserGroup:
    d = user_group_model_dict()
    return UserGroup(**d).save()


@pytest.fixture
def location_create_schema() -> LocationCreate:
    return LocationCreate(**location_schema_dict())


@pytest.fixture
def project_create_schema() -> ProjectCreate:
    return ProjectCreate(**project_schema_dict())


@pytest.fixture
def identity_service_create_schema() -> IdentityServiceCreate:
    return IdentityServiceCreate(**identity_service_schema_dict())


@pytest.fixture
def flavor_create_ext_schema() -> FlavorCreateExtended:
    return FlavorCreateExtended(**flavor_schema_dict())


@pytest.fixture
def image_create_ext_schema() -> ImageCreateExtended:
    return ImageCreateExtended(**image_schema_dict())


@pytest.fixture
def identity_provider_create_ext_schema(
    user_group_create_ext_schema: UserGroupCreateExtended,
) -> IdentityProviderCreateExtended:
    return IdentityProviderCreateExtended(
        **identity_provider_schema_dict(),
        relationship=auth_method_dict(),
        user_groups=[user_group_create_ext_schema],
    )


@pytest.fixture
def network_create_ext_schema() -> NetworkCreateExtended:
    return NetworkCreateExtended(**network_schema_dict())


@pytest.fixture
def block_storage_quota_create_ext_schema() -> BlockStorageQuotaCreateExtended:
    return BlockStorageQuotaCreateExtended(project=uuid4())


@pytest.fixture
def compute_quota_create_ext_schema() -> ComputeQuotaCreateExtended:
    return ComputeQuotaCreateExtended(project=uuid4())


@pytest.fixture
def network_quota_create_ext_schema() -> NetworkQuotaCreateExtended:
    return NetworkQuotaCreateExtended(project=uuid4())


@pytest.fixture
def region_create_ext_schema() -> RegionCreateExtended:
    return RegionCreateExtended(**region_schema_dict())


@pytest.fixture
def block_storage_service_create_ext_schema() -> BlockStorageServiceCreateExtended:
    return BlockStorageServiceCreateExtended(**block_storage_service_schema_dict())


@pytest.fixture
def compute_service_create_ext_schema() -> ComputeServiceCreateExtended:
    return ComputeServiceCreateExtended(**compute_service_schema_dict())


@pytest.fixture
def network_service_create_ext_schema() -> NetworkServiceCreateExtended:
    return NetworkServiceCreateExtended(**network_service_schema_dict())


@pytest.fixture
def sla_create_ext_schema() -> SLACreateExtended:
    return SLACreateExtended(**sla_schema_dict(), project=uuid4())


@pytest.fixture
def user_group_create_ext_schema(
    sla_create_ext_schema: SLACreateExtended,
) -> UserGroupCreateExtended:
    return UserGroupCreateExtended(
        **user_group_schema_dict(), sla=sla_create_ext_schema
    )
