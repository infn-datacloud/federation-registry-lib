from pytest_cases import case, parametrize

from fedreg.location.models import Location
from fedreg.service.enum import ServiceType
from fedreg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
)
from tests.models.utils import location_model_dict, service_model_dict


class CaseAttr:
    @case(tags="location")
    @parametrize(presence=(True, False))
    def case_regions(self, presence: bool) -> Location | None:
        return Location(**location_model_dict()).save() if presence else None

    @case(tags="services")
    @parametrize(len=(0, 1, 2))
    def case_block_storage_services(self, len: int) -> list[BlockStorageService]:
        return [
            BlockStorageService(**service_model_dict(ServiceType.BLOCK_STORAGE)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    @parametrize(len=(0, 1, 2))
    def case_compute_services(self, len: int) -> list[ComputeService]:
        return [
            ComputeService(**service_model_dict(ServiceType.COMPUTE)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    @parametrize(len=(0, 1, 2))
    def case_identity_services(self, len: int) -> list[IdentityService]:
        return [
            IdentityService(**service_model_dict(ServiceType.IDENTITY)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    @parametrize(len=(0, 1, 2))
    def case_network_services(self, len: int) -> list[NetworkService]:
        return [
            NetworkService(**service_model_dict(ServiceType.NETWORK)).save()
            for _ in range(len)
        ]

    @case(tags="services")
    @parametrize(len=(0, 1, 2))
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
