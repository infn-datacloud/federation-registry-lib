from pytest_cases import case, parametrize

from fedreg.identity_provider.models import IdentityProvider
from fedreg.location.models import Location
from fedreg.project.models import Project
from fedreg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
)
from fedreg.region.models import Region
from fedreg.service.enum import ServiceType
from fedreg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
)
from fedreg.sla.models import SLA
from fedreg.user_group.models import UserGroup
from tests.models.utils import (
    identity_provider_model_dict,
    location_model_dict,
    project_model_dict,
    quota_model_dict,
    region_model_dict,
    service_model_dict,
    sla_model_dict,
    user_group_model_dict,
)


class CaseAttr:
    @case(tags="regions")
    @parametrize(len=(1, 2))
    def case_regions(self, len: int) -> list[Region]:
        return [Region(**region_model_dict()).save() for _ in range(len)]

    @case(tags="projects")
    @parametrize(len=(1, 2))
    def case_projects(self, len: int) -> list[Project]:
        return [Project(**project_model_dict()).save() for _ in range(len)]

    @case(tags="identity_providers")
    @parametrize(len=(1, 2))
    def case_identity_providers(self, len: int) -> list[IdentityProvider]:
        return [
            IdentityProvider(**identity_provider_model_dict()).save()
            for _ in range(len)
        ]

    @case(tags="location")
    @parametrize(presence=(True, False))
    def case_location(self, presence: bool) -> Location | None:
        return Location(**location_model_dict()).save() if presence else None

    @case(tags="services")
    @parametrize(len=(1, 2))
    def case_block_storage_services(self, len: int) -> list[BlockStorageService]:
        return [
            BlockStorageService(**service_model_dict(ServiceType.BLOCK_STORAGE)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    @parametrize(len=(1, 2))
    def case_compute_services(self, len: int) -> list[ComputeService]:
        return [
            ComputeService(**service_model_dict(ServiceType.COMPUTE)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    @parametrize(len=(1, 2))
    def case_identity_services(self, len: int) -> list[IdentityService]:
        return [
            IdentityService(**service_model_dict(ServiceType.IDENTITY)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    @parametrize(len=(1, 2))
    def case_network_services(self, len: int) -> list[NetworkService]:
        return [
            NetworkService(**service_model_dict(ServiceType.NETWORK)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    @parametrize(len=(1, 2))
    def case_object_store_services(self, len: int) -> list[ObjectStoreService]:
        return [
            ObjectStoreService(**service_model_dict(ServiceType.OBJECT_STORE)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    def case_services(
        self,
        block_storage_service_model: BlockStorageService,
        compute_service_model: ComputeService,
        identity_service_model: IdentityService,
        network_service_model: NetworkService,
        object_store_service_model: ObjectStoreService,
    ) -> list[
        BlockStorageService
        | ComputeService
        | IdentityService
        | NetworkService
        | ObjectStoreService
    ]:
        return [
            block_storage_service_model,
            compute_service_model,
            identity_service_model,
            network_service_model,
            object_store_service_model,
        ]

    @case(tags=("quotas", "block-storage"))
    @parametrize(len=(1, 2))
    def case_block_storage_quota(self, len: int) -> list[BlockStorageQuota]:
        return [BlockStorageQuota(**quota_model_dict()).save() for _ in range(len)]

    @case(tags=("quotas", "compute"))
    @parametrize(len=(1, 2))
    def case_compute_quota(self, len: int) -> list[ComputeQuota]:
        return [ComputeQuota(**quota_model_dict()).save() for _ in range(len)]

    @case(tags=("quotas", "network"))
    @parametrize(len=(1, 2))
    def case_network_quota(self, len: int) -> list[NetworkQuota]:
        return [NetworkQuota(**quota_model_dict()).save() for _ in range(len)]

    @case(tags=("quotas", "object-store"))
    @parametrize(len=(1, 2))
    def case_object_store_quota(self, len: int) -> list[ObjectStoreQuota]:
        return [ObjectStoreQuota(**quota_model_dict()).save() for _ in range(len)]

    @case(tags="user_groups")
    @parametrize(len=(1, 2))
    def case_user_group(self, len: int) -> list[UserGroup]:
        return [UserGroup(**user_group_model_dict()).save() for _ in range(len)]

    @case(tags="slas")
    @parametrize(len=(1, 2))
    def case_slas(self, len: int) -> list[SLA]:
        return [SLA(**sla_model_dict()).save() for _ in range(len)]
