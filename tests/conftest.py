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
    flavor_schema_dict,
    identity_provider_schema_dict,
    identity_service_schema_dict,
    image_schema_dict,
    location_schema_dict,
    network_schema_dict,
    network_service_schema_dict,
    project_schema_dict,
    region_schema_dict,
    sla_schema_dict,
    user_group_schema_dict,
)
from tests.create_model import (
    block_storage_quota_neomodel,
    block_storage_service_neomodel,
    compute_quota_neomodel,
    compute_service_neomodel,
    flavor_neomodel,
    identity_provider_neomodel,
    identity_service_neomodel,
    image_neomodel,
    location_neomodel,
    network_neomodel,
    network_quota_neomodel,
    network_service_neomodel,
    project_neomodel,
    provider_neomodel,
    region_neomodel,
    sla_neomodel,
    user_group_neomodel,
)

DB_VERSION = "5"


@pytest.fixture(autouse=True)
def clear_os_environment() -> None:
    """Clear the OS environment."""
    os.environ.clear()


@pytest.fixture(scope="session")
def db_core() -> Generator[MagicMock, Any, None]:
    with patch("neomodel.core.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=DB_VERSION)
        yield mock_db


@pytest.fixture(scope="session")
def db_match() -> Generator[MagicMock, Any, None]:
    with patch("neomodel.match.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=DB_VERSION)
        yield mock_db


@pytest.fixture(scope="session")
def db_rel_mgr() -> Generator[MagicMock, Any, None]:
    with patch("neomodel.relationship_manager.db") as mock_db:
        type(mock_db).database_version = PropertyMock(return_value=DB_VERSION)

        d = {}
        cls_registry = MagicMock()
        cls_registry.__getitem__.side_effect = d.__getitem__
        cls_registry.__setitem__.side_effect = d.__setitem__
        mock_db._NODE_CLASS_REGISTRY = cls_registry

        yield mock_db


@pytest.fixture
def flavor_model(db_core: MagicMock) -> Flavor:
    return flavor_neomodel(db_core)


@pytest.fixture
def identity_provider_model(db_core: MagicMock) -> IdentityProvider:
    return identity_provider_neomodel(db_core)


@pytest.fixture
def image_model(db_core: MagicMock) -> Image:
    return image_neomodel(db_core)


@pytest.fixture
def location_model(db_core: MagicMock) -> Location:
    return location_neomodel(db_core)


@pytest.fixture
def network_model(db_core: MagicMock) -> Network:
    return network_neomodel(db_core)


@pytest.fixture
def project_model(db_core: MagicMock) -> Project:
    return project_neomodel(db_core)


@pytest.fixture
def provider_model(db_core: MagicMock) -> Provider:
    return provider_neomodel(db_core)


@pytest.fixture
def block_storage_quota_model(db_core: MagicMock) -> BlockStorageQuota:
    return block_storage_quota_neomodel(db_core)


@pytest.fixture
def compute_quota_model(db_core: MagicMock) -> ComputeQuota:
    return compute_quota_neomodel(db_core)


@pytest.fixture
def network_quota_model(db_core: MagicMock) -> NetworkQuota:
    return network_quota_neomodel(db_core)


@pytest.fixture
def region_model(db_core: MagicMock) -> Region:
    return region_neomodel(db_core)


@pytest.fixture
def block_storage_service_model(db_core: MagicMock) -> BlockStorageService:
    return block_storage_service_neomodel(db_core)


@pytest.fixture
def compute_service_model(db_core: MagicMock) -> ComputeService:
    return compute_service_neomodel(db_core)


@pytest.fixture
def identity_service_model(db_core: MagicMock) -> IdentityService:
    return identity_service_neomodel(db_core)


@pytest.fixture
def network_service_model(db_core: MagicMock) -> NetworkService:
    return network_service_neomodel(db_core)


@pytest.fixture
def sla_model(db_core: MagicMock) -> SLA:
    return sla_neomodel(db_core)


@pytest.fixture
def user_group_model(db_core: MagicMock) -> UserGroup:
    return user_group_neomodel(db_core)


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
