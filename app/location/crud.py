from .models import Location as LocationModel
from .schemas import LocationCreate, LocationUpdate
from ..crud import CRUDBase


class CRUDLocation(CRUDBase[LocationModel, LocationCreate, LocationUpdate]):
    """"""


location = CRUDLocation(LocationModel, LocationCreate)
