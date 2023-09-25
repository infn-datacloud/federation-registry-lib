from typing import Dict, List

from cruds.core import BasicCRUD
from cruds.flavor import FlavorCRUD
from cruds.image import ImageCRUD
from cruds.network import NetworkCRUD
from cruds.quota import BlockStorageQuotaCRUD, ComputeQuotaCRUD
from models.cmdb.project import ProjectRead
from models.cmdb.region import RegionRead
from models.cmdb.service import (
    BlockStorageServiceQuery,
    BlockStorageServiceRead,
    BlockStorageServiceWrite,
    ComputeServiceQuery,
    ComputeServiceRead,
    ComputeServiceWrite,
    IdentityServiceQuery,
    IdentityServiceRead,
    IdentityServiceWrite,
    NetworkServiceQuery,
    NetworkServiceRead,
    NetworkServiceWrite,
)
from models.config import URLs


class BlockStorageServiceCRUD(
    BasicCRUD[
        BlockStorageServiceWrite, BlockStorageServiceRead, BlockStorageServiceQuery
    ]
):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=BlockStorageServiceRead,
            write_schema=BlockStorageServiceWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.services,
            parent_url=cmdb_urls.regions,
        )
        self.quotas = BlockStorageQuotaCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def synchronize(
        self,
        *,
        items: List[BlockStorageServiceWrite],
        parent: RegionRead,
        projects: List[ProjectRead],
    ) -> List[BlockStorageServiceRead]:
        updated_items = []
        db_items = {
            db_item.endpoint: db_item
            for db_item in parent.services
            if isinstance(db_item, BlockStorageServiceRead)
        }
        for item in items:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
                new_data.quotas = self.quotas.synchronize(
                    items=item.quotas, parent=new_data, projects=projects
                )
            updated_items.append(new_data)
        for db_item in db_items:
            self.remove(item=db_item)
        return updated_items


class ComputeServiceCRUD(
    BasicCRUD[ComputeServiceWrite, ComputeServiceRead, ComputeServiceQuery]
):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=ComputeServiceRead,
            write_schema=ComputeServiceWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.services,
            parent_url=cmdb_urls.regions,
        )
        self.flavors = FlavorCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.images = ImageCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )
        self.quotas = ComputeQuotaCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def synchronize(
        self,
        *,
        items: List[ComputeServiceWrite],
        parent: RegionRead,
        projects: List[ProjectRead],
    ) -> List[ComputeServiceRead]:
        updated_items = []
        db_items = {
            db_item.endpoint: db_item
            for db_item in parent.services
            if isinstance(db_item, ComputeServiceRead)
        }
        for item in items:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
                new_data.flavors = self.flavors.synchronize(
                    items=item.flavors, parent=new_data, projects=projects
                )
                new_data.images = self.images.synchronize(
                    items=item.images, parent=new_data, projects=projects
                )
                new_data.quotas = self.quotas.synchronize(
                    items=item.quotas, parent=new_data, projects=projects
                )
            updated_items.append(new_data)
        for db_item in db_items:
            self.remove(item=db_item)
        return updated_items


class IdentityServiceCRUD(
    BasicCRUD[IdentityServiceWrite, IdentityServiceRead, IdentityServiceQuery]
):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=IdentityServiceRead,
            write_schema=IdentityServiceWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.services,
            parent_url=cmdb_urls.regions,
        )

    def synchronize(
        self, *, items: List[IdentityServiceWrite], parent: RegionRead
    ) -> List[IdentityServiceRead]:
        updated_items = []
        db_items = {
            db_item.endpoint: db_item
            for db_item in parent.services
            if isinstance(db_item, IdentityServiceRead)
        }
        for item in items:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
            updated_items.append(new_data)
        for db_item in db_items:
            self.remove(item=db_item)
        return updated_items


class NetworkServiceCRUD(
    BasicCRUD[NetworkServiceWrite, NetworkServiceRead, NetworkServiceQuery]
):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=NetworkServiceRead,
            write_schema=NetworkServiceWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.services,
            parent_url=cmdb_urls.regions,
        )
        self.networks = NetworkCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def synchronize(
        self,
        *,
        items: List[NetworkServiceWrite],
        parent: RegionRead,
        projects: List[ProjectRead],
    ) -> List[NetworkServiceRead]:
        updated_items = []
        db_items = {
            db_item.endpoint: db_item
            for db_item in parent.services
            if isinstance(db_item, NetworkServiceRead)
        }
        for item in items:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
                new_data.networks = self.networks.synchronize(
                    items=item.networks, parent=new_data, project=projects
                )
            updated_items.append(new_data)
        for db_item in db_items:
            self.remove(item=db_item)
        return updated_items
