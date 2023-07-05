from .models import Quota as QuotaModel
from .schemas import QuotaCreate, QuotaUpdate
from ..crud import CRUDBase


class CRUDQuota(CRUDBase[QuotaModel, QuotaCreate, QuotaUpdate]):
    """"""


quota = CRUDQuota(QuotaModel, QuotaCreate)
