from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb.identity_provider import IdentityProviderRead
from models.cmdb.user_group import UserGroupQuery, UserGroupRead, UserGroupWrite
from pydantic import AnyHttpUrl


class UserGroupCRUD(BasicCRUD[UserGroupWrite, UserGroupRead, UserGroupQuery]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=UserGroupRead,
            write_schema=UserGroupWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(
        self, *, item: UserGroupWrite, parent: IdentityProviderRead
    ) -> IdentityProviderRead:
        db_item, idx = self.find_in_list(
            data=UserGroupQuery(name=item.name), db_items=parent.user_groups
        )
        new_data = super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )
        if db_item is None:
            parent.user_groups.append(new_data)
        else:
            parent.user_groups[idx] = new_data
        return parent
