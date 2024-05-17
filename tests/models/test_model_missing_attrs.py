import pytest
from neomodel import RequiredProperty, StructuredNode
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.flavor.models import Flavor
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.image.models import Image
from fed_reg.location.models import Location
from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStorageQuota,
)
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStorageService,
)
from fed_reg.sla.models import SLA
from fed_reg.user_group.models import UserGroup
from tests.create_dict import (
    block_storage_quota_model_dict,
    block_storage_service_model_dict,
    compute_quota_model_dict,
    compute_service_model_dict,
    flavor_model_dict,
    identity_provider_model_dict,
    identity_service_model_dict,
    image_model_dict,
    location_model_dict,
    network_model_dict,
    network_quota_model_dict,
    network_service_model_dict,
    object_storage_quota_model_dict,
    object_storage_service_model_dict,
    project_model_dict,
    provider_model_dict,
    region_model_dict,
    sla_model_dict,
    user_group_model_dict,
)


class CaseMissing:
    @parametrize(attr=["name", "uuid"])
    def case_flavor(self, attr: str) -> tuple[dict, type[Flavor], str]:
        return flavor_model_dict(), Flavor, attr

    @parametrize(attr=["endpoint", "group_claim"])
    def case_identity_provider(
        self, attr: str
    ) -> tuple[dict, type[IdentityProvider], str]:
        return identity_provider_model_dict(), IdentityProvider, attr

    @parametrize(attr=["name", "uuid"])
    def case_image(self, attr: str) -> tuple[dict, type[Image], str]:
        return image_model_dict(), Image, attr

    @parametrize(attr=["site", "country"])
    def case_location(self, attr: str) -> tuple[dict, type[Location], str]:
        return location_model_dict(), Location, attr

    @parametrize(attr=["name", "uuid"])
    def case_network(self, attr: str) -> tuple[dict, type[Network], str]:
        return network_model_dict(), Network, attr

    @parametrize(attr=["name", "uuid"])
    def case_project(self, attr: str) -> tuple[dict, type[Project], str]:
        return project_model_dict(), Project, attr

    @parametrize(attr=["name", "type"])
    def case_provider(self, attr: str) -> tuple[dict, type[Provider], str]:
        return provider_model_dict(), Provider, attr

    @parametrize(attr=["type"])
    def case_block_storage_quota(
        self, attr: str
    ) -> tuple[dict, type[BlockStorageQuota], str]:
        return block_storage_quota_model_dict(), BlockStorageQuota, attr

    @parametrize(attr=["type"])
    def case_compute_quota(self, attr: str) -> tuple[dict, type[ComputeQuota], str]:
        return compute_quota_model_dict(), ComputeQuota, attr

    @parametrize(attr=["type"])
    def case_network_quota(self, attr: str) -> tuple[dict, type[NetworkQuota], str]:
        return network_quota_model_dict(), NetworkQuota, attr

    @parametrize(attr=["type"])
    def case_object_storage_quota(
        self, attr: str
    ) -> tuple[dict, type[ObjectStorageQuota], str]:
        return object_storage_quota_model_dict(), ObjectStorageQuota, attr

    @parametrize(attr=["name"])
    def case_region(self, attr: str) -> tuple[dict, type[Region], str]:
        return region_model_dict(), Region, attr

    @parametrize(attr=["name", "type", "endpoint"])
    def case_block_storage_service(
        self, attr: str
    ) -> tuple[dict, type[BlockStorageService], str]:
        return block_storage_service_model_dict(), BlockStorageService, attr

    @parametrize(attr=["name", "type", "endpoint"])
    def case_compute_service(self, attr: str) -> tuple[dict, type[ComputeService], str]:
        return compute_service_model_dict(), ComputeService, attr

    @parametrize(attr=["name", "type", "endpoint"])
    def case_identity_service(
        self, attr: str
    ) -> tuple[dict, type[IdentityService], str]:
        return identity_service_model_dict(), IdentityService, attr

    @parametrize(attr=["name", "type", "endpoint"])
    def case_network_service(self, attr: str) -> tuple[dict, type[NetworkService], str]:
        return network_service_model_dict(), NetworkService, attr

    @parametrize(attr=["name", "type", "endpoint"])
    def case_object_storage_service(
        self, attr: str
    ) -> tuple[dict, type[ObjectStorageService], str]:
        return object_storage_service_model_dict(), ObjectStorageService, attr

    @parametrize(attr=["doc_uuid", "start_date", "end_date"])
    def case_sla(self, attr: str) -> tuple[dict, type[SLA], str]:
        return sla_model_dict(), SLA, attr

    @parametrize(attr=["name"])
    def case_user_group(self, attr: str) -> tuple[dict, type[UserGroup], str]:
        return user_group_model_dict(), UserGroup, attr


@parametrize_with_cases("data, model, attr", cases=CaseMissing)
def test_missing_attr(data: dict, model: type[StructuredNode], attr: str) -> None:
    data[attr] = None
    item = model(**data)
    with pytest.raises(RequiredProperty):
        item.save()
