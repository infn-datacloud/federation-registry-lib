from typing import List

from app.crud import CRUDBase
from app.location.crud import location
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import RegionCreateExtended
from app.region.models import Region
from app.region.schemas import (
    RegionCreate,
    RegionRead,
    RegionReadPublic,
    RegionReadShort,
    RegionUpdate,
)
from app.region.schemas_extended import RegionReadExtended, RegionReadExtendedPublic
from app.service.crud import (
    block_storage_service,
    compute_service,
    identity_service,
    network_service,
    service,
)


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
        self,
        *,
        obj_in: RegionCreateExtended,
        provider: Provider,
        projects: List[Project],
        force: bool = False
    ) -> Region:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        if obj_in.location is not None:
            location.create(obj_in=obj_in.location, region=db_obj)
        for item in obj_in.block_storage_services:
            block_storage_service.create(
                obj_in=item, region=db_obj, projects=projects, force=True
            )
        for item in obj_in.compute_services:
            compute_service.create(
                obj_in=item, region=db_obj, projects=projects, force=True
            )
        for item in obj_in.identity_services:
            identity_service.create(obj_in=item, region=db_obj, force=True)
        for item in obj_in.network_services:
            network_service.create(obj_in=item, region=db_obj, force=True)
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
