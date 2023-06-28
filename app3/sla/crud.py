from typing import List, Tuple

from .models import SLA as SLAModel
from .schemas import SLACreate, SLAUpdate
from .schemas_extended import SLACreateExtended
from ..crud import CRUDBase
from ..project.models import Project as ProjectModel
from ..quota.schemas_extended import QuotaCreateExtended
from ..quota.crud import quota
from ..quota_type.models import QuotaType as QuotaTypeModel
from ..service.models import Service as ServiceModel
from ..user_group.models import UserGroup as UserGroupModel


class CRUDSLA(CRUDBase[SLAModel, SLACreate, SLAUpdate]):
    """"""

    def create_and_connect_quotas(
        self,
        *,
        db_obj: SLAModel,
        new_items: List[
            Tuple[QuotaCreateExtended, QuotaTypeModel, ServiceModel]
        ]
    ) -> None:
        for q, qt, srv in new_items:
            db_quota = quota.create(obj_in=q)
            db_quota.type.connect(qt)
            db_quota.service.connect(srv)
            db_obj.quotas.connect(db_quota)

    def create_with_all(
        self,
        *,
        sla: SLACreateExtended,
        project: ProjectModel,
        user_group: UserGroupModel,
        quotas: List[Tuple[QuotaCreateExtended, QuotaTypeModel, ServiceModel]]
    ) -> SLAModel:
        db_obj = self.create(obj_in=sla)
        db_obj.project.connect(project)
        db_obj.user_group.connect(user_group)
        self.create_and_connect_quotas(db_obj=db_obj, new_items=quotas)
        return db_obj


sla = CRUDSLA(SLAModel, SLACreate)
