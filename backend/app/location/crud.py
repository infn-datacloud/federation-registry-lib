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
from app.location.schemas_extended import (
    LocationReadExtended,
    LocationReadExtendedPublic,
)
from app.region.models import Region


class CRUDLocation(
    CRUDBase[
        Location,
        LocationCreate,
        LocationUpdate,
        LocationRead,
        LocationReadPublic,
        LocationReadShort,
        LocationReadExtended,
        LocationReadExtendedPublic,
    ]
):
    """"""

    def create(
        self,
        *,
        obj_in: LocationCreate,
        region: Optional[Region] = None,
        force: bool = False
    ) -> Location:
        db_obj = super().create(obj_in=obj_in, force=force)
        if region is not None:
            db_obj.regions.connect(region)
        return db_obj


location = CRUDLocation(
    model=Location,
    create_schema=LocationCreate,
    read_schema=LocationRead,
    read_public_schema=LocationReadPublic,
    read_short_schema=LocationReadShort,
    read_extended_schema=LocationReadExtended,
    read_extended_public_schema=LocationReadExtendedPublic,
)
