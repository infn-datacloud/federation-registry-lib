from typing import List

from .models import ServiceType as ServiceTypeModel
from .schemas import ServiceTypeCreate
from .schemas_extended import ServiceTypeCreateExtended
from ..crud import CRUDBase
from ..quota_type.crud import quota_type
from ..quota_type.schemas import QuotaTypeCreate


class CRUDServiceType(
    CRUDBase[ServiceTypeModel, ServiceTypeCreate, ServiceTypeCreate]
):
    """"""

    def create_and_connect_service_type_to_quota_types(
        self, *, db_obj: ServiceTypeModel, qtypes: List[QuotaTypeCreate]
    ) -> None:
        for qtype in qtypes:
            db_qt = quota_type.create(obj_in=qtype)
            if not db_obj.quota_types.is_connected(db_qt):
                db_obj.quota_types.connect(db_qt)

    def create_with_quotas(
        self, *, obj_in: ServiceTypeCreateExtended
    ) -> ServiceTypeModel:
        db_obj = self.create(obj_in=obj_in)
        self.create_and_connect_service_type_to_quota_types(
            db_obj=db_obj, qtypes=obj_in.quota_types
        )
        return db_obj


service_type = CRUDServiceType(ServiceTypeModel, ServiceTypeCreate)
