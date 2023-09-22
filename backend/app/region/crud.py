from app.crud import CRUDBase
from app.location.crud import location
from app.provider.models import Provider
from app.region.models import Region
from app.region.schemas import (
    RegionCreate,
    RegionRead,
    RegionReadPublic,
    RegionReadShort,
    RegionUpdate,
)
from app.region.schemas_extended import RegionReadExtended, RegionReadExtendedPublic
from app.service.crud import service


class CRUDRegion(
    CRUDBase[
        Region,
        RegionCreate,
        RegionUpdate,
        RegionRead,
        RegionReadPublic,
        RegionReadShort,
        RegionReadExtended,
        RegionReadExtendedPublic,
    ]
):
    """"""

    def create(
        self, *, obj_in: RegionCreate, provider: Provider, force: bool = False
    ) -> Region:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj

    def remove(self, *, db_obj: Region, from_provider: bool = False) -> bool:
        # If the corresponding provider has no other regions,
        # abort region deletion in favor of provider deletion.
        if not from_provider:
            item = db_obj.provider.single()
            if len(item.regions.all()) == 1:
                return False

        for item in db_obj.services.all():
            service.remove(db_obj=item)
        result = super().remove(db_obj=db_obj)
        item = db_obj.location.single()
        if item is not None:
            if len(item.regions.all()) == 0:
                location.remove(db_obj=item)
        return result


region = CRUDRegion(
    model=Region,
    create_schema=RegionCreate,
    read_schema=RegionRead,
    read_public_schema=RegionReadPublic,
    read_short_schema=RegionReadShort,
    read_extended_schema=RegionReadExtended,
    read_extended_public_schema=RegionReadExtendedPublic,
)
