from typing import Dict, List

from cruds.core import BasicCRUD
from cruds.location import LocationCRUD
from cruds.service import (
    BlockStorageServiceCRUD,
    ComputeServiceCRUD,
    IdentityServiceCRUD,
    NetworkServiceCRUD,
)
from models.cmdb.provider import ProviderRead
from models.cmdb.region import RegionQuery, RegionRead, RegionWrite
from models.config import URLs


class RegionCRUD(BasicCRUD[RegionWrite, RegionRead, RegionQuery]):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=RegionRead,
            write_schema=RegionWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.regions,
            parent_url=cmdb_urls.providers,
        )
        self.locations = LocationCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.block_storage_services = BlockStorageServiceCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.compute_services = ComputeServiceCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.identity_services = IdentityServiceCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.network_services = NetworkServiceCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def synchronize(
        self, *, items: List[RegionWrite], parent: ProviderRead
    ) -> List[RegionRead]:
        updated_items = []
        db_items = {db_item.name: db_item for db_item in parent.regions}
        for item in items:
            db_item = db_items.pop(item.name, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
                new_data.location = self.locations.synchronize(
                    item=item.location, parent=new_data
                )
                new_data.services = (
                    self.block_storage_services.synchronize(
                        item=item.block_storage_services,
                        parent=new_data,
                        projects=parent.projects,
                    )
                    + self.compute_services.synchronize(
                        item=item.compute_services,
                        parent=new_data,
                        projects=parent.projects,
                    )
                    + self.identity_services.synchronize(
                        item=item.identity_services, parent=new_data
                    )
                    + self.network_services.synchronize(
                        item=item.network_services, parent=new_data
                    )
                )
            updated_items.append(new_data)
        for db_item in db_items:
            self.remove(item=db_item)
        return updated_items
