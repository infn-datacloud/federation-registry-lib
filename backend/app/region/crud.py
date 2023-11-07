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
from app.region.schemas_extended import (
    RegionReadExtended,
    RegionReadExtendedPublic,
)
from app.service.crud import (
    block_storage_service,
    compute_service,
    identity_service,
    network_service,
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
    """Region Create, Read, Update and Delete operations."""

    def create(self, *, obj_in: RegionCreateExtended, provider: Provider) -> Region:
        """Create a new Region.

        Connect the region to the given provider. For each received location and
        service, create the corresponding entity.
        """
        db_obj = super().create(obj_in=obj_in)
        db_obj.provider.connect(provider)
        if obj_in.location is not None:
            location.create(obj_in=obj_in.location, region=db_obj)
        for item in obj_in.block_storage_services:
            block_storage_service.create(
                obj_in=item, region=db_obj, projects=provider.projects
            )
        for item in obj_in.compute_services:
            compute_service.create(
                obj_in=item, region=db_obj, projects=provider.projects
            )
        for item in obj_in.identity_services:
            identity_service.create(obj_in=item, region=db_obj)
        for item in obj_in.network_services:
            network_service.create(
                obj_in=item, region=db_obj, projects=provider.projects
            )
        return db_obj

    def remove(self, *, db_obj: Region, from_provider: bool = False) -> bool:
        """Delete an existing region and all its relationships.

        If the corresponding provider has no other regions, abort region deletion in
        favor of provider deletion.

        At first delete its services. Then, if the location points only to this
        provider, delete it. Finally delete the region.
        """
        if not from_provider:
            item = db_obj.provider.single()
            if len(item.regions) == 1:
                return False

        for db_serv in db_obj.services:
            if isinstance(db_serv, BlockStorageService):
                block_storage_service.remove(db_obj=db_serv)
            elif isinstance(db_serv, ComputeService):
                compute_service.remove(db_obj=db_serv)
            elif isinstance(db_serv, IdentityService):
                identity_service.remove(db_obj=db_serv)
            elif isinstance(db_serv, NetworkService):
                network_service.remove(db_obj=db_serv)

        item = db_obj.location.single()
        if item and len(item.regions) == 1:
            location.remove(db_obj=item)

        result = super().remove(db_obj=db_obj)
        return result

    def update(
        self,
        *,
        db_obj: Region,
        obj_in: Union[RegionCreateExtended, RegionUpdate],
        projects: Optional[List[Project]] = None,
        force: bool = False,
    ) -> Optional[Region]:
        """Update Region attributes.

        By default do not update relationships or default values. If force is True,
        update linked projects and apply default values when explicit.
        """
        if projects is None:
            projects = []
        edit = False
        if force:
            locations_updated = self.__update_location(db_obj=db_obj, obj_in=obj_in)
            bsto_serv_updated = self.__update_block_storage_services(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )
            comp_serv_updated = self.__update_compute_services(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )
            idp_serv_updated = self.__update_identity_services(
                db_obj=db_obj, obj_in=obj_in
            )
            net_serv_updated = self.__update_network_services(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )
            edit = (
                locations_updated
                or bsto_serv_updated
                or comp_serv_updated
                or idp_serv_updated
                or net_serv_updated
            )

        if isinstance(obj_in, RegionCreateExtended):
            obj_in = RegionUpdate.parse_obj(obj_in)

        update_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else update_data

    def __update_location(
        self, *, db_obj: Region, obj_in: RegionCreateExtended
    ) -> bool:
        """Update region linked location.

        If no new location is given or the new location differs from the current one,
        delete linked location if it points only to this region, or disconnect it.

        If there wasn't a location and and a new one is given, or the new location
        differs from the current one, create the new location. Otherwise, if the old
        location match the new location, forcefully update it.
        """
        edit = False
        loc_in = obj_in.location
        db_loc = db_obj.location.single()

        if db_loc and (not loc_in or db_loc.site != loc_in.site):
            if len(db_loc.regions) == 1:
                location.remove(db_obj=db_loc)
            else:
                db_obj.location.disconnect(db_loc)
            edit = True

        # No previous and new location received
        # or new location differs from existing one
        if (not db_loc and loc_in) or (
            db_loc and loc_in and db_loc.site != loc_in.site
        ):
            location.create(obj_in=loc_in, region=db_obj)
            edit = True
        elif db_loc and loc_in and db_loc.site == loc_in.site:
            updated_data = location.update(db_obj=db_loc, obj_in=loc_in, force=True)
            edit = updated_data is not None

        return edit

    def __update_block_storage_services(
        self,
        *,
        db_obj: Region,
        obj_in: RegionCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        """Update region linked block storage services.

        Connect new block storage services not already connect, leave untouched already
        linked ones and delete old ones no more connected to the region.
        """
        edit = False
        db_items = {
            db_item.endpoint: db_item
            for db_item in db_obj.services
            if isinstance(db_item, BlockStorageService)
        }
        for item in obj_in.block_storage_services:
            db_item = db_items.pop(item.endpoint, None)
            if not db_item:
                block_storage_service.create(
                    obj_in=item, region=db_obj, projects=provider_projects
                )
                edit = True
            else:
                updated_data = block_storage_service.update(
                    db_obj=db_item,
                    obj_in=item,
                    projects=provider_projects,
                    force=True,
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
        """Update region linked compute services.

        Connect new compute services not already connect, leave untouched already linked
        ones and delete old ones no more connected to the region.
        """
        edit = False
        db_items = {
            db_item.endpoint: db_item
            for db_item in db_obj.services
            if isinstance(db_item, ComputeService)
        }
        for item in obj_in.compute_services:
            db_item = db_items.pop(item.endpoint, None)
            if not db_item:
                compute_service.create(
                    obj_in=item, region=db_obj, projects=provider_projects
                )
                edit = True
            else:
                updated_data = compute_service.update(
                    db_obj=db_item,
                    obj_in=item,
                    projects=provider_projects,
                    force=True,
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
        """Update region linked identity services.

        Connect new identity services not already connect, leave untouched already
        linked ones and delete old ones no more connected to the region.
        """
        edit = False
        db_items = {
            db_item.endpoint: db_item
            for db_item in db_obj.services
            if isinstance(db_item, IdentityService)
        }
        for item in obj_in.identity_services:
            db_item = db_items.pop(item.endpoint, None)
            if not db_item:
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
        """Update region linked network services.

        Connect new network services not already connect, leave untouched already linked
        ones and delete old ones no more connected to the region.
        """
        edit = False
        db_items = {
            db_item.endpoint: db_item
            for db_item in db_obj.services
            if isinstance(db_item, NetworkService)
        }
        for item in obj_in.network_services:
            db_item = db_items.pop(item.endpoint, None)
            if not db_item:
                network_service.create(
                    obj_in=item, region=db_obj, projects=provider_projects
                )
                edit = True
            else:
                updated_data = network_service.update(
                    db_obj=db_item,
                    obj_in=item,
                    projects=provider_projects,
                    force=True,
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
