from pytest_cases import case

from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
)
from tests.create_dict import (
    block_storage_service_model_dict,
    compute_service_model_dict,
    identity_service_model_dict,
    network_service_model_dict,
    object_store_service_model_dict,
)


class CaseServices:
    @case(tags=["single"])
    def case_block_storage_service(
        self, block_storage_service_model: BlockStorageService
    ) -> BlockStorageService:
        return block_storage_service_model

    @case(tags=["single"])
    def case_compute_service(
        self, compute_service_model: ComputeService
    ) -> ComputeService:
        return compute_service_model

    @case(tags=["single"])
    def case_identity_service(
        self, identity_service_model: IdentityService
    ) -> IdentityService:
        return identity_service_model

    @case(tags=["single"])
    def case_network_service(
        self, network_service_model: NetworkService
    ) -> NetworkService:
        return network_service_model

    @case(tags=["single"])
    def case_object_store_service(
        self, object_store_service_model: ObjectStoreService
    ) -> ObjectStoreService:
        return object_store_service_model

    @case(tags=["multi"])
    def case_block_storage_services(self) -> list[BlockStorageService]:
        return [
            BlockStorageService(**block_storage_service_model_dict()).save(),
            BlockStorageService(**block_storage_service_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_compute_services(self) -> list[ComputeService]:
        return [
            ComputeService(**compute_service_model_dict()).save(),
            ComputeService(**compute_service_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_identity_services(self) -> list[IdentityService]:
        return [
            IdentityService(**identity_service_model_dict()).save(),
            IdentityService(**identity_service_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_network_services(self) -> list[NetworkService]:
        return [
            NetworkService(**network_service_model_dict()).save(),
            NetworkService(**network_service_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_object_store_services(self) -> list[ObjectStoreService]:
        return [
            ObjectStoreService(**object_store_service_model_dict()).save(),
            ObjectStoreService(**object_store_service_model_dict()).save(),
        ]
