from pytest_cases import case, parametrize

from fedreg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
)
from tests.v1.models.utils import quota_model_dict


class CaseAttr:
    @case(tags=("quotas", "block_storage"))
    @parametrize(len=(0, 1, 2))
    def case_block_storage_quotas(self, len: int) -> list[BlockStorageQuota]:
        return [BlockStorageQuota(**quota_model_dict()).save() for _ in range(len)]

    @case(tags=("quotas", "compute"))
    @parametrize(len=(0, 1, 2))
    def case_compute_quotas(self, len: int) -> list[ComputeQuota]:
        return [ComputeQuota(**quota_model_dict()).save() for _ in range(len)]

    @case(tags=("quotas", "network"))
    @parametrize(len=(0, 1, 2))
    def case_network_quotas(self, len: int) -> list[NetworkQuota]:
        return [NetworkQuota(**quota_model_dict()).save() for _ in range(len)]

    @case(tags=("quotas", "object_store"))
    @parametrize(len=(0, 1, 2))
    def case_object_store_quotas(self, len: int) -> list[ObjectStoreQuota]:
        return [ObjectStoreQuota(**quota_model_dict()).save() for _ in range(len)]
