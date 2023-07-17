from .models import SLA as SLAModel
from .schemas import SLACreate, SLAUpdate
from ..crud import CRUDBase


class CRUDSLA(CRUDBase[SLAModel, SLACreate, SLAUpdate]):
    """"""


sla = CRUDSLA(SLAModel, SLACreate)
