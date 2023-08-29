from typing import Optional

from app.crud import CRUDBase
from app.location.models import Location
from app.location.schemas import LocationCreate, LocationUpdate
from app.provider.models import Provider


class CRUDLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):
    """"""

    def create(
        self,
        *,
        obj_in: LocationCreate,
        provider: Optional[Provider] = None,
        force: bool = False
    ) -> Location:
        db_obj = super().create(obj_in=obj_in, force=force)
        if provider is not None:
            db_obj.providers.connect(provider)
        return db_obj


location = CRUDLocation(Location, LocationCreate)
