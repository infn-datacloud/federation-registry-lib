from app.crud import CRUDBase
from app.project.models import Project
from app.project.schemas_extended import QuotaReadExtended, QuotaReadExtendedPublic
from app.quota.models import NovaQuota, Quota
from app.quota.schemas import (
    NovaQuotaCreate,
    NovaQuotaRead,
    NovaQuotaReadPublic,
    NovaQuotaReadShort,
    NovaQuotaUpdate,
    QuotaCreate,
    QuotaRead,
    QuotaReadPublic,
    QuotaReadShort,
    QuotaUpdate,
)
from app.quota.schemas_extended import (
    NovaQuotaReadExtended,
    NovaQuotaReadExtendedPublic,
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
        QuotaReadExtended,
        QuotaReadExtendedPublic,
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
        if isinstance(obj_in, NovaQuotaCreate):
            db_obj = nova_quota.create(obj_in=obj_in, force=force)
        db_obj.service.connect(service)
        db_obj.project.connect(project)
        return db_obj


class CRUDNovaQuota(
    CRUDBase[
        NovaQuota,
        NovaQuotaCreate,
        NovaQuotaUpdate,
        NovaQuotaRead,
        NovaQuotaReadPublic,
        NovaQuotaReadShort,
        NovaQuotaReadExtended,
        NovaQuotaReadExtendedPublic,
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
    read_extended_public_schema=QuotaReadExtendedPublic,
)
nova_quota = CRUDNovaQuota(
    model=NovaQuota,
    create_schema=NovaQuotaCreate,
    read_schema=NovaQuotaRead,
    read_public_schema=NovaQuotaReadPublic,
    read_short_schema=NovaQuotaReadShort,
    read_extended_schema=NovaQuotaReadExtended,
    read_extended_public_schema=NovaQuotaReadExtendedPublic,
)
