from .models import QuotaType as QuotaTypeModel
from .schemas import QuotaTypeCreate, QuotaTypeUpdate
from ..crud import CRUDBase


class CRUDQuotaType(
    CRUDBase[QuotaTypeModel, QuotaTypeCreate, QuotaTypeUpdate]
):
    """"""


quota_type = CRUDQuotaType(QuotaTypeModel, QuotaTypeCreate)
