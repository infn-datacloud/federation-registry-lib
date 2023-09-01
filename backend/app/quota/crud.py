from app.crud import CRUDBase
from app.project.models import Project
from app.project.schemas_extended import QuotaReadExtended
from app.quota.models import NumCPUQuota, Quota, RAMQuota
from app.quota.schemas import (
    NumCPUQuotaCreate,
    NumCPUQuotaRead,
    NumCPUQuotaReadPublic,
    NumCPUQuotaReadShort,
    NumCPUQuotaUpdate,
    QuotaCreate,
    QuotaRead,
    QuotaReadPublic,
    QuotaReadShort,
    QuotaUpdate,
    RAMQuotaCreate,
    RAMQuotaRead,
    RAMQuotaReadPublic,
    RAMQuotaReadShort,
    RAMQuotaUpdate,
)
from app.quota.schemas_extended import NumCPUQuotaReadExtended, RAMQuotaReadExtended
from app.service.models import Service


class CRUDQuota(
    CRUDBase[
        Quota,
        QuotaCreate,
        QuotaUpdate,
        QuotaRead,
        QuotaReadPublic,
        QuotaReadShort,
        QuotaReadExtended,
        None,
    ]
):
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
    CRUDBase[
        NumCPUQuota,
        NumCPUQuotaCreate,
        NumCPUQuotaUpdate,
        NumCPUQuotaRead,
        NumCPUQuotaReadPublic,
        NumCPUQuotaReadShort,
        NumCPUQuotaReadExtended,
        None,
    ]
):
    """"""


class CRUDRAMQuota(
    CRUDBase[
        RAMQuota,
        RAMQuotaCreate,
        RAMQuotaUpdate,
        RAMQuotaRead,
        RAMQuotaReadPublic,
        RAMQuotaReadShort,
        RAMQuotaReadExtended,
        None,
    ]
):
    """"""


quota = CRUDQuota(
    model=Quota,
    create_schema=QuotaCreate,
    read_schema=QuotaRead,
    read_public_schema=QuotaReadPublic,
    read_short_schema=QuotaReadShort,
    read_extended_schema=QuotaReadExtended,
    read_extended_public_schema=None,
)
num_cpu_quota = CRUDNumCPUQuota(
    model=NumCPUQuota,
    create_schema=NumCPUQuotaCreate,
    read_schema=NumCPUQuotaRead,
    read_public_schema=NumCPUQuotaReadPublic,
    read_short_schema=NumCPUQuotaReadShort,
    read_extended_schema=NumCPUQuotaReadExtended,
    read_extended_public_schema=None,
)
ram_quota = CRUDRAMQuota(
    model=RAMQuota,
    create_schema=RAMQuotaCreate,
    read_schema=RAMQuotaRead,
    read_public_schema=RAMQuotaReadPublic,
    read_short_schema=RAMQuotaReadShort,
    read_extended_schema=RAMQuotaReadExtended,
    read_extended_public_schema=None,
)
