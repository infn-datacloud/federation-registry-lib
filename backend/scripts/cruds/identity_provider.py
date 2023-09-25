from typing import Dict, List

from cruds.core import BasicCRUD
from cruds.user_group import UserGroupCRUD
from models.cmdb.identity_provider import (
    IdentityProviderQuery,
    IdentityProviderRead,
    IdentityProviderWrite,
)
from models.cmdb.provider import ProviderRead
from models.config import URLs


class IdentityProviderCRUD(
    BasicCRUD[IdentityProviderWrite, IdentityProviderRead, IdentityProviderQuery]
):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str]
    ) -> None:
        super().__init__(
            read_schema=IdentityProviderRead,
            write_schema=IdentityProviderWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.identity_providers,
            parent_url=cmdb_urls.providers,
            connectable_items=["providers"],
        )
        self.user_groups = UserGroupCRUD(
            cmdb_urls=cmdb_urls,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def synchronize(
        self, *, items: List[IdentityProviderWrite], parent: ProviderRead
    ) -> List[IdentityProviderRead]:
        updated_items = []
        db_items = {db_item.endpoint: db_item for db_item in parent.identity_providers}
        for item in items:
            db_item = db_items.pop(item.endpoint, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
                new_data.user_groups = self.user_groups.synchronize(
                    items=item.user_groups, parent=new_data, projects=parent.projects
                )
            updated_items.append(new_data)
        for db_item in db_items:
            self.disconnect(item=db_item)
            # TODO Verify to delete all orphan idps
        return updated_items
