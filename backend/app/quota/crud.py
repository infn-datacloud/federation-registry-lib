from typing import Any, Dict, Optional, Union

from app.crud import CRUDBase
from app.project.models import Project
from app.quota.models import BlockStorageQuota, ComputeQuota, Quota
from app.quota.schemas import (
    BlockStorageQuotaCreate,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaReadShort,
    BlockStorageQuotaUpdate,
    ComputeQuotaCreate,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaReadShort,
    ComputeQuotaUpdate,
    QuotaCreate,
    QuotaRead,
    QuotaReadPublic,
    QuotaReadShort,
    QuotaUpdate,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from app.service.models import Service


class CRUDQuota(
    CRUDBase[
        Quota,
        QuotaCreate,
        QuotaUpdate,
        QuotaRead,
        QuotaReadPublic,
        QuotaReadShort,
        None,
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
        if isinstance(obj_in, BlockStorageQuotaCreate):
            db_obj = block_storage_quota.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, ComputeQuotaCreate):
            db_obj = nova_quota.create(obj_in=obj_in, force=force)
        db_obj.service.connect(service)
        db_obj.project.connect(project)
        return db_obj

    def remove(self, *, db_obj: Quota) -> bool:
        if isinstance(db_obj, BlockStorageQuota):
            return block_storage_quota.remove(db_obj=db_obj)
        elif isinstance(db_obj, ComputeQuota):
            return nova_quota.remove(db_obj=db_obj)

    def update(
        self, *, db_obj: Quota, obj_in: Union[QuotaUpdate, Dict[str, Any]]
    ) -> Optional[Quota]:
        if isinstance(db_obj, BlockStorageQuota):
            return block_storage_quota.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, ComputeQuota):
            return nova_quota.update(db_obj=db_obj, obj_in=obj_in)


class CRUDBlockStorageQuota(
    CRUDBase[
        BlockStorageQuota,
        BlockStorageQuotaCreate,
        BlockStorageQuotaUpdate,
        BlockStorageQuotaRead,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadShort,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadExtendedPublic,
    ]
):
    """"""


class CRUDComputeQuota(
    CRUDBase[
        ComputeQuota,
        ComputeQuotaCreate,
        ComputeQuotaUpdate,
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadShort,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
    ]
):
    """"""


quota = CRUDQuota(
    model=Quota,
    create_schema=QuotaCreate,
    read_schema=QuotaRead,
    read_public_schema=QuotaReadPublic,
    read_short_schema=QuotaReadShort,
    read_extended_schema=None,
    read_extended_public_schema=None,
)
block_storage_quota = CRUDBlockStorageQuota(
    model=BlockStorageQuota,
    create_schema=BlockStorageQuotaCreate,
    read_schema=BlockStorageQuotaRead,
    read_public_schema=BlockStorageQuotaReadPublic,
    read_short_schema=BlockStorageQuotaReadShort,
    read_extended_schema=BlockStorageQuotaReadExtended,
    read_extended_public_schema=BlockStorageQuotaReadExtendedPublic,
)
nova_quota = CRUDComputeQuota(
    model=ComputeQuota,
    create_schema=ComputeQuotaCreate,
    read_schema=ComputeQuotaRead,
    read_public_schema=ComputeQuotaReadPublic,
    read_short_schema=ComputeQuotaReadShort,
    read_extended_schema=ComputeQuotaReadExtended,
    read_extended_public_schema=ComputeQuotaReadExtendedPublic,
)
