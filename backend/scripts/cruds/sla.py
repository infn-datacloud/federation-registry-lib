from typing import Dict, List

from cruds.core import BasicCRUD
from models.cmdb.project import ProjectRead
from models.cmdb.sla import SLAQuery, SLARead, SLAWrite
from models.cmdb.user_group import UserGroupRead
from models.config import URLs


class SLACRUD(BasicCRUD[SLAWrite, SLARead, SLAQuery]):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=SLARead,
            write_schema=SLAWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.slas,
        )

    def synchronize(
        self,
        *,
        items: List[SLAWrite],
        parent: UserGroupRead,
        projects: List[ProjectRead],
    ) -> List[SLARead]:
        updated_items = []
        db_items = {db_item.doc_uuid: db_item for db_item in parent.slas}
        db_projects = {p.uuid: p for p in projects}
        for item in items:
            db_item = db_items.pop(item.doc_uuid, None)
            db_project = db_projects.get(item.project)
            if db_item is None:
                new_data = self.create(
                    new_data=item,
                    params={"project_uid": db_project.uid, "user_goup_uid": parent.uid},
                )
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
            updated_items.append(new_data)
        for db_sla in db_items.values():
            self.remove(item=db_sla)
        return updated_items
