from app.crud import CRUDBase
from app.quota.models import NumCPUQuota, Quota, RAMQuota
from app.quota.schemas import (
    NumCPUQuotaCreate,
    NumCPUQuotaUpdate,
    QuotaCreate,
    QuotaUpdate,
    RAMQuotaCreate,
    RAMQuotaUpdate,
)


class CRUDQuota(CRUDBase[Quota, QuotaCreate, QuotaUpdate]):
    """"""


class CRUDNumCPUQuota(
    CRUDBase[NumCPUQuota, NumCPUQuotaCreate, NumCPUQuotaUpdate]
):
    """"""


class CRUDRAMQuota(CRUDBase[RAMQuota, RAMQuotaCreate, RAMQuotaUpdate]):
    """"""


quota = CRUDQuota(Quota, QuotaCreate)
num_cpu_quota = CRUDNumCPUQuota(NumCPUQuota, NumCPUQuotaCreate)
ram_quota = CRUDRAMQuota(RAMQuota, RAMQuotaCreate)
