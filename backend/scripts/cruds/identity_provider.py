from typing import Dict

from cruds.core import Connectable
from models.cmdb.identity_provider import (
    IdentityProviderQuery,
    IdentityProviderRead,
    IdentityProviderWrite,
)
from models.cmdb.provider import ProviderRead
from pydantic import AnyHttpUrl


class IdentityProviderCRUD(
    Connectable[IdentityProviderWrite, IdentityProviderRead, IdentityProviderQuery]
):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        connect_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=IdentityProviderRead,
            write_schema=IdentityProviderWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            connect_url=connect_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(
        self, *, item: IdentityProviderWrite, parent: ProviderRead
    ) -> ProviderRead:
        db_item = self.single(
            data=IdentityProviderQuery(endpoint=item.endpoint), with_conn=True
        )
        new_data = super().create_or_update(item=item, db_item=db_item)
        self.connect(
            uid=new_data.uid, parent_uid=parent.uid, conn_data=item.relationship
        )

        db_item, idx = self.find_in_list(
            data=IdentityProviderQuery(endpoint=item.endpoint),
            db_items=parent.identity_providers,
        )
        if db_item is None:
            parent.identity_providers.append(new_data)
        else:
            parent.identity_providers[idx] = new_data
        return parent
