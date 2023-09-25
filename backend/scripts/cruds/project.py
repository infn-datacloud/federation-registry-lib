from typing import Dict, List

from cruds.core import BasicCRUD
from models.cmdb.project import ProjectQuery, ProjectRead, ProjectWrite
from models.cmdb.provider import ProviderRead
from models.config import URLs


class ProjectCRUD(BasicCRUD[ProjectWrite, ProjectRead, ProjectQuery]):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=ProjectRead,
            write_schema=ProjectWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.projects,
            parent_url=cmdb_urls.providers,
        )

    def synchronize(
        self, *, items: List[ProjectWrite], parent: ProviderRead
    ) -> List[ProjectRead]:
        updated_items = []
        db_items = {db_item.uuid: db_item for db_item in parent.projects}
        for item in items:
            db_item = db_items.pop(item.uuid, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
            updated_items.append(new_data)
        for db_item in db_items:
            self.remove(item=db_item)
        return updated_items
