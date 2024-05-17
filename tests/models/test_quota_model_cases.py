from fed_reg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStorageQuota,
)


class CaseQuotaModel:
    def case_block_storage_quota(
        self, block_storage_quota_model: BlockStorageQuota
    ) -> BlockStorageQuota:
        return block_storage_quota_model

    def case_compute_quota(self, compute_quota_model: ComputeQuota) -> ComputeQuota:
        return compute_quota_model

    def case_network_quota(self, network_quota_model: NetworkQuota) -> NetworkQuota:
        return network_quota_model

    def case_object_storage_quota(
        self, object_storage_quota_model: ObjectStorageQuota
    ) -> ObjectStorageQuota:
        return object_storage_quota_model
