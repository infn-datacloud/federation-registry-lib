from app.sla.models import SLA as SLAModel
from app.sla.schemas import SLACreate, SLAUpdate
from app.crud import CRUDBase


class CRUDSLA(CRUDBase[SLAModel, SLACreate, SLAUpdate]):
    """"""


sla = CRUDSLA(SLAModel, SLACreate)
