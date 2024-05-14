import os
from typing import Any
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient
from flaat.user_infos import UserInfos
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.config import get_settings
from fed_reg.flavor.models import Flavor
from fed_reg.flavor.schemas import FlavorRead, FlavorReadPublic
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fed_reg.image.models import Image
from fed_reg.image.schemas import ImageRead, ImageReadPublic
from fed_reg.location.models import Location
from fed_reg.location.schemas import LocationRead, LocationReadPublic
from fed_reg.models import BaseNodeRead
from fed_reg.network.models import Network
from fed_reg.network.schemas import NetworkRead, NetworkReadPublic
from fed_reg.project.models import Project
from fed_reg.project.schemas import ProjectRead, ProjectReadPublic
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas import ProviderRead, ProviderReadPublic
from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from fed_reg.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
)
from fed_reg.region.models import Region
from fed_reg.region.schemas import RegionRead, RegionReadPublic
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from fed_reg.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)
from fed_reg.sla.models import SLA
from fed_reg.sla.schemas import SLARead, SLAReadPublic
from fed_reg.user_group.models import UserGroup
from fed_reg.user_group.schemas import UserGroupRead, UserGroupReadPublic


class CaseSingleMulti:
    @parametrize(single=[True, False])
    def case_single_multi(self, single: bool) -> bool:
        return single


class CaseItemEndpointSchemaPublic:
    def case_flavor(
        self, flavor_model: Flavor
    ) -> tuple[Flavor, str, type[FlavorReadPublic]]:
        return flavor_model, "flavors", FlavorReadPublic

    def case_identity_provider(
        self, identity_provider_model: IdentityProvider
    ) -> tuple[IdentityProvider, str, type[IdentityProviderReadPublic]]:
        return (
            identity_provider_model,
            "identity_providers",
            IdentityProviderReadPublic,
        )

    def case_image(
        self, image_model: Image
    ) -> tuple[Image, str, type[ImageReadPublic]]:
        return image_model, "images", ImageReadPublic

    def case_location(
        self, location_model: Location
    ) -> tuple[Location, str, type[LocationReadPublic]]:
        return location_model, "locations", LocationReadPublic

    def case_network(
        self, network_model: Network
    ) -> tuple[Network, str, type[NetworkReadPublic]]:
        return network_model, "networks", NetworkReadPublic

    def case_project(
        self, project_model: Project
    ) -> tuple[Project, str, type[ProjectReadPublic]]:
        return project_model, "projects", ProjectReadPublic

    def case_provider(
        self, provider_model: Provider
    ) -> tuple[Provider, str, type[ProviderReadPublic]]:
        return provider_model, "providers", ProviderReadPublic

    def case_block_storage_quota(
        self, block_storage_quota_model: BlockStorageQuota
    ) -> tuple[BlockStorageQuota, str, type[BlockStorageQuotaReadPublic]]:
        return (
            block_storage_quota_model,
            "block_storage_quotas",
            BlockStorageQuotaReadPublic,
        )

    def case_compute_quota(
        self, compute_quota_model: ComputeQuota
    ) -> tuple[ComputeQuota, str, type[ComputeQuotaReadPublic]]:
        return compute_quota_model, "compute_quotas", ComputeQuotaReadPublic

    def case_network_quota(
        self, network_quota_model: NetworkQuota
    ) -> tuple[NetworkQuota, str, type[NetworkQuotaReadPublic]]:
        return network_quota_model, "network_quotas", NetworkQuotaReadPublic

    def case_region(
        self, region_model: Region
    ) -> tuple[Region, str, type[RegionReadPublic]]:
        return region_model, "regions", RegionReadPublic

    def case_block_storage_service(
        self, block_storage_service_model: BlockStorageService
    ) -> tuple[BlockStorageService, str, type[BlockStorageServiceReadPublic]]:
        return (
            block_storage_service_model,
            "block_storage_services",
            BlockStorageServiceReadPublic,
        )

    def case_compute_service(
        self, compute_service_model: ComputeService
    ) -> tuple[ComputeService, str, type[ComputeServiceReadPublic]]:
        return (compute_service_model, "compute_services", ComputeServiceReadPublic)

    def case_identity_service(
        self, identity_service_model: IdentityService
    ) -> tuple[IdentityService, str, type[IdentityServiceReadPublic]]:
        return (identity_service_model, "identity_services", IdentityServiceReadPublic)

    def case_network_service(
        self, network_service_model: NetworkService
    ) -> tuple[NetworkService, str, type[NetworkServiceReadPublic]]:
        return (network_service_model, "network_services", NetworkServiceReadPublic)

    def case_sla(self, sla_model: SLA) -> tuple[SLA, str, type[SLAReadPublic]]:
        return sla_model, "slas", SLAReadPublic

    def case_user_group(
        self, user_group_model: UserGroup
    ) -> tuple[UserGroup, str, type[UserGroupReadPublic]]:
        return user_group_model, "user_groups", UserGroupReadPublic


class CaseItemEndpointSchemaDir:
    def case_flavor(
        self, flavor_model: Flavor
    ) -> tuple[Flavor, str, type[FlavorRead], str]:
        return flavor_model, "flavors", FlavorRead, "flavor"

    def case_identity_provider(
        self, identity_provider_model: IdentityProvider
    ) -> tuple[IdentityProvider, str, type[IdentityProviderRead], str]:
        return (
            identity_provider_model,
            "identity_providers",
            IdentityProviderRead,
            "identity_provider",
        )

    def case_image(self, image_model: Image) -> tuple[Image, str, type[ImageRead], str]:
        return image_model, "images", ImageRead, "image"

    def case_location(
        self, location_model: Location
    ) -> tuple[Location, str, type[LocationRead], str]:
        return location_model, "locations", LocationRead, "location"

    def case_network(
        self, network_model: Network
    ) -> tuple[Network, str, type[NetworkRead], str]:
        return network_model, "networks", NetworkRead, "network"

    def case_project(
        self, project_model: Project
    ) -> tuple[Project, str, type[ProjectRead], str]:
        return project_model, "projects", ProjectRead, "project"

    def case_provider(
        self, provider_model: Provider
    ) -> tuple[Provider, str, type[ProviderRead], str]:
        return provider_model, "providers", ProviderRead, "provider"

    def case_block_storage_quota(
        self, block_storage_quota_model: BlockStorageQuota
    ) -> tuple[BlockStorageQuota, str, type[BlockStorageQuotaRead], str]:
        return (
            block_storage_quota_model,
            "block_storage_quotas",
            BlockStorageQuotaRead,
            "quota",
        )

    def case_compute_quota(
        self, compute_quota_model: ComputeQuota
    ) -> tuple[ComputeQuota, str, type[ComputeQuotaRead], str]:
        return compute_quota_model, "compute_quotas", ComputeQuotaRead, "quota"

    def case_network_quota(
        self, network_quota_model: NetworkQuota
    ) -> tuple[NetworkQuota, str, type[NetworkQuotaRead], str]:
        return network_quota_model, "network_quotas", NetworkQuotaRead, "quota"

    def case_region(
        self, region_model: Region
    ) -> tuple[Region, str, type[RegionRead], str]:
        return region_model, "regions", RegionRead, "region"

    def case_block_storage_service(
        self, block_storage_service_model: BlockStorageService
    ) -> tuple[BlockStorageService, str, type[BlockStorageServiceRead], str]:
        return (
            block_storage_service_model,
            "block_storage_services",
            BlockStorageServiceRead,
            "service",
        )

    def case_compute_service(
        self, compute_service_model: ComputeService
    ) -> tuple[ComputeService, str, type[ComputeServiceRead], str]:
        return (
            compute_service_model,
            "compute_services",
            ComputeServiceRead,
            "service",
        )

    def case_identity_service(
        self, identity_service_model: IdentityService
    ) -> tuple[IdentityService, str, type[IdentityServiceRead], str]:
        return (
            identity_service_model,
            "identity_services",
            IdentityServiceRead,
            "service",
        )

    def case_network_service(
        self, network_service_model: NetworkService
    ) -> tuple[NetworkService, str, type[NetworkServiceRead], str]:
        return (
            network_service_model,
            "network_services",
            NetworkServiceRead,
            "service",
        )

    def case_sla(self, sla_model: SLA) -> tuple[SLA, str, type[SLARead], str]:
        return sla_model, "slas", SLARead, "sla"

    def case_user_group(
        self, user_group_model: UserGroup
    ) -> tuple[UserGroup, str, type[UserGroupRead], str]:
        return user_group_model, "user_groups", UserGroupRead, "user_group"


@parametrize_with_cases("single", cases=CaseSingleMulti)
@parametrize_with_cases("item, endpoint, schema", cases=CaseItemEndpointSchemaPublic)
def test_get_no_authn_verify_class(
    client_no_authn: TestClient,
    single: bool,
    item: Any,
    endpoint: str,
    schema: type[BaseNodeRead],
):
    settings = get_settings()
    if single:
        url = os.path.join(settings.API_V1_STR, endpoint, item.uid)
    else:
        url = os.path.join(settings.API_V1_STR, endpoint)
    resp = client_no_authn.get(url)
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    if single:
        assert data is not None
    else:
        assert len(data) > 0
        data = data[0]

    fields = {**schema.__fields__}
    for k in data:
        fields.pop(k)
    assert not fields


@parametrize_with_cases("single", cases=CaseSingleMulti)
@parametrize_with_cases("item, endpoint, schema, dir", cases=CaseItemEndpointSchemaDir)
def test_get_authn_verify_class(
    client_with_token: TestClient,
    user_infos_with_read_email: UserInfos,
    single: bool,
    item: Any,
    endpoint: str,
    schema: type[BaseNodeRead],
    dir: str,
):
    settings = get_settings()
    if single:
        url = os.path.join(settings.API_V1_STR, endpoint, item.uid)
    else:
        url = os.path.join(settings.API_V1_STR, endpoint)

    with patch(
        f"fed_reg.{dir}.api.v1.endpoints.flaat.get_user_infos_from_request",
        return_value=user_infos_with_read_email,
    ):
        resp = client_with_token.get(url)
    assert resp.status_code == status.HTTP_200_OK

    data = resp.json()
    if single:
        assert data is not None
    else:
        assert len(data) > 0
        data = data[0]

    fields = {**schema.__fields__}
    for k in data:
        fields.pop(k)
    assert not fields
