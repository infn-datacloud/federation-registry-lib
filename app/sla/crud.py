from app.sla.models import SLA 
from app.sla.schemas import SLACreate, SLAUpdate
from app.crud import CRUDBase


class CRUDSLA(CRUDBase[SLA, SLACreate, SLAUpdate]):
    """"""


sla = CRUDSLA(SLA, SLACreate)
