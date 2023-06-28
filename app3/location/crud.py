from .models import Location as LocationModel
from .schemas import LocationCreate, LocationPatch
from ..crud import CRUDBase


class CRUDLocation(CRUDBase[LocationModel, LocationCreate, LocationPatch]):
    """"""


location = CRUDLocation(LocationModel, LocationCreate)
