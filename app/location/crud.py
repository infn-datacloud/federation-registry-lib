from app.location.models import Location as LocationModel
from app.location.schemas import LocationCreate, LocationUpdate
from app.crud import CRUDBase


class CRUDLocation(CRUDBase[LocationModel, LocationCreate, LocationUpdate]):
    """"""


location = CRUDLocation(LocationModel, LocationCreate)
