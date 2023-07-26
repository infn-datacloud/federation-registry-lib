from app.crud import CRUDBase
from app.project.models import Project
from app.quota.models import NumCPUQuota, Quota, RAMQuota
from app.quota.schemas import (
    NumCPUQuotaCreate,
    NumCPUQuotaUpdate,
    QuotaCreate,
    QuotaUpdate,
    RAMQuotaCreate,
    RAMQuotaUpdate,
)
from app.service.models import Service


class CRUDQuota(CRUDBase[Quota, QuotaCreate, QuotaUpdate]):
    """"""

    def create(
        self,
        *,
        obj_in: QuotaCreate,
        project: Project,
        service: Service,
        force: bool = False
    ) -> Quota:
        if isinstance(obj_in, NumCPUQuotaCreate):
            db_obj = num_cpu_quota.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, RAMQuotaCreate):
            db_obj = ram_quota.create(obj_in=obj_in, force=force)
        db_obj.project.connect(project)
        db_obj.service.connect(service)
        return db_obj


class CRUDNumCPUQuota(
    CRUDBase[NumCPUQuota, NumCPUQuotaCreate, NumCPUQuotaUpdate]
):
    """"""


class CRUDRAMQuota(CRUDBase[RAMQuota, RAMQuotaCreate, RAMQuotaUpdate]):
    """"""


quota = CRUDQuota(Quota, QuotaCreate)
num_cpu_quota = CRUDNumCPUQuota(NumCPUQuota, NumCPUQuotaCreate)
ram_quota = CRUDRAMQuota(RAMQuota, RAMQuotaCreate)
