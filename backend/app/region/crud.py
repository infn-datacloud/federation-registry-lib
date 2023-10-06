from typing import List, Optional, Union

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
from app.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
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

    def create(self, *, obj_in: RegionCreateExtended, provider: Provider) -> Region:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.provider.connect(provider)
        if obj_in.location is not None:
            location.create(obj_in=obj_in.location, region=db_obj)
        for item in obj_in.block_storage_services:
            block_storage_service.create(
                obj_in=item, region=db_obj, projects=provider.projects.all()
            )
        for item in obj_in.compute_services:
            compute_service.create(
                obj_in=item, region=db_obj, projects=provider.projects.all()
            )
        for item in obj_in.identity_services:
            identity_service.create(obj_in=item, region=db_obj)
        for item in obj_in.network_services:
            network_service.create(
                obj_in=item, region=db_obj, projects=provider.projects.all()
            )
        return db_obj

    def remove(self, *, db_obj: Region, from_provider: bool = False) -> bool:
        # If the corresponding provider has no other regions,
        # abort region deletion in favor of provider deletion.
        if not from_provider:
            item = db_obj.provider.single()
            if len(item.regions) == 1:
                return False

        for item in db_obj.services:
            service.remove(db_obj=item)
        item = db_obj.location.single()
        if item is not None:
            if len(item.regions) == 1:
                location.remove(db_obj=item)
        result = super().remove(db_obj=db_obj)
        return result

    def update(
        self,
        *,
        db_obj: Region,
        obj_in: Union[RegionCreateExtended, RegionUpdate],
        projects: List[Project] = [],
        force: bool = False
    ) -> Optional[Region]:
        if force:
            # Location
            item = obj_in.location
            if item is not None:
                db_item = location.get(site=item.site)
                if db_item is None:
                    location.create(obj_in=item, region=db_obj)
                else:
                    location.update(db_obj=db_item, obj_in=item, force=force)
                    db_obj.location.connect(db_item)
            else:
                db_item = db_obj.location.single()
                if db_item:
                    if len(db_item.regions) == 1:
                        location.remove(db_item)
                    else:
                        db_obj.location.disconnect(db_item)

            # Block Storage Service
            db_items = {
                db_item.endpoint: db_item
                for db_item in db_obj.services
                if isinstance(db_item, BlockStorageService)
            }
            for item in obj_in.block_storage_services:
                db_item = db_items.pop(item.endpoint, None)
                if db_item is None:
                    block_storage_service.create(obj_in=item, region=db_obj)
                else:
                    block_storage_service.update(
                        db_obj=db_item, obj_in=item, projects=projects, force=force
                    )
            for db_item in db_items:
                block_storage_service.remove(db_obj=db_item)

            # Compute Service
            db_items = {
                db_item.endpoint: db_item
                for db_item in db_obj.services
                if isinstance(db_item, ComputeService)
            }
            for item in obj_in.compute_services:
                db_item = db_items.pop(item.endpoint, None)
                if db_item is None:
                    compute_service.create(obj_in=item, region=db_obj)
                else:
                    compute_service.update(
                        db_obj=db_item, obj_in=item, projects=projects, force=force
                    )
            for db_item in db_items:
                compute_service.remove(db_obj=db_item)

            # Identity Service
            db_items = {
                db_item.endpoint: db_item
                for db_item in db_obj.services
                if isinstance(db_item, IdentityService)
            }
            for item in obj_in.identity_services:
                db_item = db_items.pop(item.endpoint, None)
                if db_item is None:
                    identity_service.create(obj_in=item, region=db_obj)
                else:
                    identity_service.update(db_obj=db_item, obj_in=item, force=force)
            for db_item in db_items:
                identity_service.remove(db_obj=db_item)

            # Network Service
            db_items = {
                db_item.endpoint: db_item
                for db_item in db_obj.services
                if isinstance(db_item, NetworkService)
            }
            for item in obj_in.network_services:
                db_item = db_items.pop(item.endpoint, None)
                if db_item is None:
                    network_service.create(obj_in=item, region=db_obj)
                else:
                    network_service.update(
                        db_obj=db_item, obj_in=item, projects=projects, force=force
                    )
            for db_item in db_items:
                network_service.remove(db_obj=db_item)
        return super().update(db_obj=db_obj, obj_in=obj_in, force=force)


region = CRUDRegion(
    model=Region,
    create_schema=RegionCreate,
    read_schema=RegionRead,
    read_public_schema=RegionReadPublic,
    read_short_schema=RegionReadShort,
    read_extended_schema=RegionReadExtended,
    read_extended_public_schema=RegionReadExtendedPublic,
)
