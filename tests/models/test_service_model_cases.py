from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
)


class CaseServiceModel:
    def case_block_storage_service(
        self, block_storage_service_model: BlockStorageService
    ) -> BlockStorageService:
        return block_storage_service_model

    def case_compute_service(
        self, compute_service_model: ComputeService
    ) -> ComputeService:
        return compute_service_model

    def case_identity_service(
        self, identity_service_model: IdentityService
    ) -> IdentityService:
        return identity_service_model

    def case_network_service(
        self, network_service_model: NetworkService
    ) -> NetworkService:
        return network_service_model

    def case_object_store_service(
        self, object_store_service_model: ObjectStoreService
    ) -> ObjectStoreService:
        return object_store_service_model
