from typing import Optional

from app.crud import CRUDBase
from app.location.models import Location
from app.location.schemas import (
    LocationCreate,
    LocationRead,
    LocationReadPublic,
    LocationReadShort,
    LocationUpdate,
)
from app.location.schemas_extended import LocationReadExtended
from app.provider.models import Provider


class CRUDLocation(
    CRUDBase[
        Location,
        LocationCreate,
        LocationUpdate,
        LocationRead,
        LocationReadPublic,
        LocationReadShort,
        LocationReadExtended,
    ]
):
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


location = CRUDLocation(
    model=Location,
    create_schema=LocationCreate,
    read_schema=LocationRead,
    read_public_schema=LocationReadPublic,
    read_short_schema=LocationReadShort,
    read_extended_schema=LocationReadExtended,
)
