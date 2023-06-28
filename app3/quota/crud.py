from .models import Quota as QuotaModel
from .schemas import QuotaCreate
from ..crud import CRUDBase


class CRUDQuota(CRUDBase[QuotaModel, QuotaCreate, QuotaCreate]):
    """"""


quota = CRUDQuota(QuotaModel, QuotaCreate)
