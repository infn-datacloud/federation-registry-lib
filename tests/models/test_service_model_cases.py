from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    NetworkService,
    ObjectStorageService,
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

    def case_network_service(
        self, network_service_model: NetworkService
    ) -> NetworkService:
        return network_service_model

    def case_object_storage_service(
        self, object_storage_service_model: ObjectStorageService
    ) -> ObjectStorageService:
        return object_storage_service_model
