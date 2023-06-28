from .models import Service as ServiceModel
from .schemas import ServiceCreate, ServiceUpdate
from .schemas_extended import ServiceCreateExtended
from ..crud import CRUDBase
from ..service_type.crud import service_type


class CRUDService(CRUDBase[ServiceModel, ServiceCreate, ServiceUpdate]):
    """"""

    def create_with_type(
        self, *, obj_in: ServiceCreateExtended
    ) -> ServiceModel:
        db_obj = self.create(obj_in=obj_in)
        db_st = service_type.get(name=obj_in.type.name)
        db_obj.type.connect(db_st)
        return db_obj


service = CRUDService(ServiceModel, ServiceCreate)
