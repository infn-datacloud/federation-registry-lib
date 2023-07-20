from app.crud import CRUDBase
from app.sla.models import SLA 
from app.sla.schemas import SLACreate, SLAUpdate


class CRUDSLA(CRUDBase[SLA, SLACreate, SLAUpdate]):
    """"""


sla = CRUDSLA(SLA, SLACreate)
