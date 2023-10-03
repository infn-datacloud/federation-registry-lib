from typing import Dict, List

from cruds.core import BasicCRUD
from cruds.sla import SLACRUD
from models.cmdb.identity_provider import IdentityProviderRead
from models.cmdb.project import ProjectRead
from models.cmdb.user_group import UserGroupQuery, UserGroupRead, UserGroupWrite
from models.config import URLs


class UserGroupCRUD(BasicCRUD[UserGroupWrite, UserGroupRead, UserGroupQuery]):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=UserGroupRead,
            write_schema=UserGroupWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.user_groups,
            parent_url=cmdb_urls.identity_providers,
        )
        self.slas = SLACRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def synchronize(
        self,
        *,
        items: List[UserGroupWrite],
        parent: IdentityProviderRead,
        projects: List[ProjectRead],
    ) -> List[UserGroupRead]:
        updated_items = []
        db_items = {db_item.name: db_item for db_item in parent.user_groups}
        for item in items:
            db_item = db_items.pop(item.name, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
                new_data.slas = self.slas.synchronize(
                    items=item.slas, parent=new_data, projects=projects
                )
            updated_items.append(new_data)
        for db_item in db_items.values():
            self.remove(item=db_item)
        return updated_items
