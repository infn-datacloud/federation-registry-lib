from app.crud import CRUDBase
from app.quota.enum import (
    QuotaTypeBandwidth,
    QuotaTypeCount,
    QuotaTypeFrequency,
    QuotaTypeMoney,
    QuotaTypeSize,
    QuotaTypeTime,
)
from app.quota.models import NumCPUQuota, Quota as QuotaModel, RAMQuota
from app.quota.schemas import (
    NumCPUQuotaCreate,
    NumCPUQuotaUpdate,
    QuotaCreate,
    QuotaUpdate,
    RAMQuotaCreate,
    RAMQuotaUpdate,
)


class CRUDQuota(CRUDBase[QuotaModel, QuotaCreate, QuotaUpdate]):
    """"""

    def create(
        self, *, obj_in: QuotaCreate, force: bool = False
    ) -> QuotaModel:
        if obj_in.type == QuotaTypeBandwidth.download_bandwidth.value:
            pass
        elif obj_in.type == QuotaTypeBandwidth.upload_bandwidth.value:
            pass
        elif obj_in.type == QuotaTypeCount.num_cpus.value:
            return num_cpu_quota.create(obj_in=obj_in, force=force)
        elif obj_in.type == QuotaTypeCount.public_ip.value:
            pass
        elif obj_in.type == QuotaTypeFrequency.cpu_frequency.value:
            pass
        elif obj_in.type == QuotaTypeMoney.cost.value:
            pass
        elif obj_in.type == QuotaTypeSize.disk_size.value:
            pass
        elif obj_in.type == QuotaTypeSize.download_aggregated.value:
            pass
        elif obj_in.type == QuotaTypeSize.mem_size.value:
            return ram_quota.create(obj_in=obj_in, force=force)
        elif obj_in.type == QuotaTypeSize.upload_aggregated.value:
            pass
        elif obj_in.type == QuotaTypeTime.computing_time.value:
            pass
        return super().create(obj_in=obj_in, force=force)


class CRUDNumCPUQuota(
    CRUDBase[NumCPUQuota, NumCPUQuotaCreate, NumCPUQuotaUpdate]
):
    """"""


class CRUDRAMQuota(CRUDBase[RAMQuota, RAMQuotaCreate, RAMQuotaUpdate]):
    """"""


quota = CRUDQuota(QuotaModel, QuotaCreate)
num_cpu_quota = CRUDQuota(QuotaModel, QuotaCreate)
ram_quota = CRUDQuota(QuotaModel, QuotaCreate)
