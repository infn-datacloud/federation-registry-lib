from app.location.models import Location 
from app.location.schemas import LocationCreate, LocationUpdate
from app.crud import CRUDBase


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    """"""


location = CRUDLocation(Location, LocationCreate)
