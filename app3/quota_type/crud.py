from .models import QuotaType as QuotaTypeModel
from .schemas import QuotaTypeCreate, QuotaTypePatch
from ..crud import CRUDBase


class CRUDQuotaType(CRUDBase[QuotaTypeModel, QuotaTypeCreate, QuotaTypePatch]):
    """"""


quota_type = CRUDQuotaType(QuotaTypeModel, QuotaTypeCreate)
