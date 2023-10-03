from typing import Dict, List

from cruds.core import BasicCRUD
from cruds.identity_provider import IdentityProviderCRUD
from cruds.project import ProjectCRUD
from cruds.region import RegionCRUD
from models.cmdb.provider import ProviderQuery, ProviderRead, ProviderWrite
from models.config import URLs


class ProviderCRUD(BasicCRUD[ProviderWrite, ProviderRead, ProviderQuery]):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=ProviderRead,
            write_schema=ProviderWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.providers,
        )
        self.identity_providers = IdentityProviderCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.projects = ProjectCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.regions = RegionCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def synchronize(self, *, items: List[ProviderWrite]) -> List[ProviderRead]:
        updated_items = []
        db_items = {db_item.name: db_item for db_item in self.all(with_conn=True)}
        for item in items:
            db_item = db_items.pop(item.name, None)
            # Create or update
            if db_item is None:
                new_data = self.create(data=item)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
                # Sync projects, identity providers and regions
                # Projects must be synchronized first because
                # their uid will be used by later calls.
                new_data.projects = self.projects.synchronize(
                    items=item.projects, parent=new_data
                )
                new_data.identity_providers = self.identity_providers.synchronize(
                    items=item.identity_providers, parent=new_data
                )
                new_data.regions = self.regions.synchronize(
                    items=item.regions, parent=new_data
                )
            updated_items.append(new_data)
        # Delete no-more tracked items
        for db_item in db_items.values():
            self.remove(item=db_item)
        return updated_items
