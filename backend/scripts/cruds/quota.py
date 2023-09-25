from typing import Dict, List

from cruds.core import BasicCRUD
from models.cmdb.project import ProjectRead
from models.cmdb.quota import (
    BlockStorageQuotaQuery,
    BlockStorageQuotaRead,
    BlockStorageQuotaWrite,
    ComputeQuotaQuery,
    ComputeQuotaRead,
    ComputeQuotaWrite,
)
from models.cmdb.service import BlockStorageServiceRead, ComputeServiceRead
from models.config import URLs


class ComputeQuotaCRUD(
    BasicCRUD[ComputeQuotaWrite, ComputeQuotaRead, ComputeQuotaQuery]
):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=ComputeQuotaRead,
            write_schema=ComputeQuotaWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.quotas,
        )

    def synchronize(
        self,
        *,
        items: List[ComputeQuotaWrite],
        parent: ComputeServiceRead,
        projects: List[ProjectRead],
    ) -> List[ComputeQuotaRead]:
        updated_items = []
        for db_item in parent.quotas:
            self.remove(item=db_item)
        db_projects = {p.uuid: p for p in projects}
        for item in items:
            db_project = db_projects.get(item.project)
            new_data = self.create(
                new_data=item,
                params={"project_uid": db_project.uid, "service_uid": parent.uid},
            )
            updated_items.append(new_data)
        return updated_items


class BlockStorageQuotaCRUD(
    BasicCRUD[BlockStorageQuotaWrite, BlockStorageQuotaRead, BlockStorageQuotaQuery]
):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=BlockStorageQuotaRead,
            write_schema=BlockStorageQuotaWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.quotas,
        )

    def synchronize(
        self,
        *,
        items: List[BlockStorageQuotaWrite],
        parent: BlockStorageServiceRead,
        projects: List[ProjectRead],
    ) -> List[BlockStorageQuotaRead]:
        updated_items = []
        for db_item in parent.quotas:
            self.remove(item=db_item)
        db_projects = {p.uuid: p for p in projects}
        for item in items:
            db_project = db_projects.get(item.project)
            new_data = self.create(
                new_data=item,
                params={"project_uid": db_project.uid, "service_uid": parent.uid},
            )
            updated_items.append(new_data)
        return updated_items
