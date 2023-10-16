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
        force: bool = False,
    ) -> Optional[Region]:
        edit = False
        if force:
            edit = (
                edit
                or self.__update_location(db_obj=db_obj, obj_in=obj_in)
                or self.__update_block_storage_services(
                    db_obj=db_obj, obj_in=obj_in, provider_projects=projects
                )
                or self.__update_compute_services(
                    db_obj=db_obj, obj_in=obj_in, provider_projects=projects
                )
                or self.__update_identity_services(db_obj=db_obj, obj_in=obj_in)
                or self.__update_network_services(
                    db_obj=db_obj, obj_in=obj_in, provider_projects=projects
                )
            )
        update_data = super().update(
            db_obj=db_obj, obj_in=RegionUpdate.parse_obj(obj_in), force=force
        )
        return db_obj if edit else update_data

    def __update_location(
        self, *, db_obj: Region, obj_in: RegionCreateExtended
    ) -> bool:
        edit = False
        item = obj_in.location
        db_loc = db_obj.location.single()
        if db_loc:
            db_obj.location.disconnect(db_loc)
            edit = True
        if item:
            db_item = location.get(site=item.site)
            if not db_item:
                location.create(obj_in=item, region=db_obj)
                edit = True
            else:
                updated_data = location.update(db_obj=db_item, obj_in=item, force=True)
                db_obj.location.connect(db_item)
                edit = updated_data is not None
        if (
            db_loc
            and not db_obj.location.is_connected(db_loc)
            and len(db_loc.regions) == 0
        ):
            location.remove(db_obj=db_loc)
            edit = True
        return edit

    def __update_block_storage_services(
        self,
        *,
        db_obj: Region,
        obj_in: RegionCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        edit = False
        db_items = {
            db_item.endpoint: db_item
            for db_item in db_obj.services
            if isinstance(db_item, BlockStorageService)
        }
        for item in obj_in.block_storage_services:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                block_storage_service.create(
                    obj_in=item, region=db_obj, projects=provider_projects
                )
                edit = True
            else:
                updated_data = block_storage_service.update(
                    db_obj=db_item, obj_in=item, projects=provider_projects, force=True
                )
                if not edit and updated_data is not None:
                    edit = True
        for db_item in db_items.values():
            block_storage_service.remove(db_obj=db_item)
            edit = True
        return edit

    def __update_compute_services(
        self,
        *,
        db_obj: Region,
        obj_in: RegionCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        edit = False
        db_items = {
            db_item.endpoint: db_item
            for db_item in db_obj.services
            if isinstance(db_item, ComputeService)
        }
        for item in obj_in.compute_services:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                compute_service.create(
                    obj_in=item, region=db_obj, projects=provider_projects
                )
                edit = True
            else:
                updated_data = compute_service.update(
                    db_obj=db_item, obj_in=item, projects=provider_projects, force=True
                )
                if not edit and updated_data is not None:
                    edit = True
        for db_item in db_items.values():
            compute_service.remove(db_obj=db_item)
            edit = True
        return edit

    def __update_identity_services(
        self,
        *,
        db_obj: Region,
        obj_in: RegionCreateExtended,
    ) -> bool:
        edit = False
        db_items = {
            db_item.endpoint: db_item
            for db_item in db_obj.services
            if isinstance(db_item, IdentityService)
        }
        for item in obj_in.identity_services:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                identity_service.create(obj_in=item, region=db_obj)
                edit = True
            else:
                updated_data = identity_service.update(
                    db_obj=db_item, obj_in=item, force=True
                )
                if not edit and updated_data is not None:
                    edit = True
        for db_item in db_items.values():
            identity_service.remove(db_obj=db_item)
            edit = True
        return edit

    def __update_network_services(
        self,
        *,
        db_obj: Region,
        obj_in: RegionCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        edit = False
        db_items = {
            db_item.endpoint: db_item
            for db_item in db_obj.services
            if isinstance(db_item, NetworkService)
        }
        for item in obj_in.network_services:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                network_service.create(
                    obj_in=item, region=db_obj, projects=provider_projects
                )
                edit = True
            else:
                updated_data = network_service.update(
                    db_obj=db_item, obj_in=item, projects=provider_projects, force=True
                )
                if not edit and updated_data is not None:
                    edit = True
        for db_item in db_items.values():
            network_service.remove(db_obj=db_item)
        edit = True
        return edit


region = CRUDRegion(
    model=Region,
    create_schema=RegionCreate,
    read_schema=RegionRead,
    read_public_schema=RegionReadPublic,
    read_short_schema=RegionReadShort,
    read_extended_schema=RegionReadExtended,
    read_extended_public_schema=RegionReadExtendedPublic,
)
