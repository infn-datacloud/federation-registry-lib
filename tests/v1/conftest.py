"""File to set tests configuration parameters and model fixtures."""

import pytest

from fedreg.v1.flavor.models import Flavor, PrivateFlavor, SharedFlavor
from fedreg.v1.identity_provider.models import IdentityProvider
from fedreg.v1.image.models import Image, PrivateImage, SharedImage
from fedreg.v1.location.models import Location
from fedreg.v1.network.models import Network, PrivateNetwork, SharedNetwork
from fedreg.v1.project.models import Project
from fedreg.v1.provider.models import Provider
from fedreg.v1.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
    Quota,
)
from fedreg.v1.region.models import Region
from fedreg.v1.service.enum import ServiceType
from fedreg.v1.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
    Service,
)
from fedreg.v1.sla.models import SLA
from fedreg.v1.user_group.models import UserGroup
from tests.v1.models.utils import (
    flavor_model_dict,
    identity_provider_model_dict,
    image_model_dict,
    location_model_dict,
    network_model_dict,
    project_model_dict,
    provider_model_dict,
    quota_model_dict,
    region_model_dict,
    service_model_dict,
    sla_model_dict,
    user_group_model_dict,
)


@pytest.fixture
def flavor_model() -> Flavor:
    return Flavor(**flavor_model_dict()).save()


@pytest.fixture
def private_flavor_model() -> PrivateFlavor:
    return PrivateFlavor(**flavor_model_dict()).save()


@pytest.fixture
def shared_flavor_model() -> SharedFlavor:
    return SharedFlavor(**flavor_model_dict()).save()


@pytest.fixture
def identity_provider_model() -> IdentityProvider:
    return IdentityProvider(**identity_provider_model_dict()).save()


@pytest.fixture
def image_model() -> Image:
    return Image(**image_model_dict()).save()


@pytest.fixture
def private_image_model() -> PrivateImage:
    return PrivateImage(**image_model_dict()).save()


@pytest.fixture
def shared_image_model() -> SharedImage:
    return SharedImage(**image_model_dict()).save()


@pytest.fixture
def location_model() -> Location:
    return Location(**location_model_dict()).save()


@pytest.fixture
def network_model() -> Network:
    return Network(**network_model_dict()).save()


@pytest.fixture
def private_network_model() -> PrivateNetwork:
    return PrivateNetwork(**network_model_dict()).save()


@pytest.fixture
def shared_network_model() -> SharedNetwork:
    return SharedNetwork(**network_model_dict()).save()


@pytest.fixture
def project_model() -> Project:
    return Project(**project_model_dict()).save()


@pytest.fixture
def provider_model() -> Provider:
    return Provider(**provider_model_dict()).save()


@pytest.fixture
def quota_model() -> Quota:
    return Quota(**quota_model_dict()).save()


@pytest.fixture
def block_storage_quota_model() -> BlockStorageQuota:
    return BlockStorageQuota(**quota_model_dict()).save()


@pytest.fixture
def compute_quota_model() -> ComputeQuota:
    return ComputeQuota(**quota_model_dict()).save()


@pytest.fixture
def network_quota_model() -> NetworkQuota:
    return NetworkQuota(**quota_model_dict()).save()


@pytest.fixture
def object_store_quota_model() -> ObjectStoreQuota:
    return ObjectStoreQuota(**quota_model_dict()).save()


@pytest.fixture
def region_model() -> Region:
    return Region(**region_model_dict()).save()


@pytest.fixture
def service_model() -> Service:
    return Service(**service_model_dict()).save()


@pytest.fixture
def block_storage_service_model() -> BlockStorageService:
    return BlockStorageService(**service_model_dict(ServiceType.BLOCK_STORAGE)).save()


@pytest.fixture
def compute_service_model() -> ComputeService:
    return ComputeService(**service_model_dict(ServiceType.COMPUTE)).save()


@pytest.fixture
def identity_service_model() -> IdentityService:
    return IdentityService(**service_model_dict(ServiceType.IDENTITY)).save()


@pytest.fixture
def network_service_model() -> NetworkService:
    return NetworkService(**service_model_dict(ServiceType.NETWORK)).save()


@pytest.fixture
def object_store_service_model() -> ObjectStoreService:
    return ObjectStoreService(**service_model_dict(ServiceType.OBJECT_STORE)).save()


@pytest.fixture
def sla_model() -> SLA:
    return SLA(**sla_model_dict()).save()


@pytest.fixture
def user_group_model() -> UserGroup:
    return UserGroup(**user_group_model_dict()).save()
