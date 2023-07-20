from app.crud import CRUDBase
from app.location.models import Location 
from app.location.schemas import LocationCreate, LocationUpdate


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    """"""


location = CRUDLocation(Location, LocationCreate)
