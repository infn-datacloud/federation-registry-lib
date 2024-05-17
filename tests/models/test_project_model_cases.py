from pytest_cases import case

from fed_reg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStorageQuota,
)
from tests.create_dict import (
    block_storage_quota_model_dict,
    compute_quota_model_dict,
    network_quota_model_dict,
    object_storage_quota_model_dict,
)


class CaseQuotas:
    @case(tags=["single"])
    def case_block_storage_quota(
        self, block_storage_quota_model: BlockStorageQuota
    ) -> BlockStorageQuota:
        return block_storage_quota_model

    @case(tags=["single"])
    def case_compute_quota(self, compute_quota_model: ComputeQuota) -> ComputeQuota:
        return compute_quota_model

    @case(tags=["single"])
    def case_network_quota(self, network_quota_model: NetworkQuota) -> NetworkQuota:
        return network_quota_model

    @case(tags=["single"])
    def case_object_storage_quota(
        self, object_storage_quota_model: ObjectStorageQuota
    ) -> ObjectStorageQuota:
        return object_storage_quota_model

    @case(tags=["multi"])
    def case_block_storage_quotas(self) -> list[BlockStorageQuota]:
        return [
            BlockStorageQuota(**block_storage_quota_model_dict()).save(),
            BlockStorageQuota(**block_storage_quota_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_compute_quotas(self) -> list[ComputeQuota]:
        return [
            ComputeQuota(**compute_quota_model_dict()).save(),
            ComputeQuota(**compute_quota_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_network_quotas(self) -> list[NetworkQuota]:
        return [
            NetworkQuota(**network_quota_model_dict()).save(),
            NetworkQuota(**network_quota_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_object_storage_quotas(self) -> list[ObjectStorageQuota]:
        return [
            ObjectStorageQuota(**object_storage_quota_model_dict()).save(),
            ObjectStorageQuota(**object_storage_quota_model_dict()).save(),
        ]
