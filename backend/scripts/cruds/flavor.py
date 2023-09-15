from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb import FlavorQuery, FlavorRead, FlavorWrite, ProviderRead
from pydantic import AnyHttpUrl


class FlavorCRUD(BasicCRUD[FlavorWrite, FlavorRead, FlavorQuery]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Flavor",
            read_schema=FlavorRead,
            write_schema=FlavorWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(
        self, *, item: FlavorWrite, parent: ProviderRead
    ) -> FlavorRead:
        db_item = self.find_in_list(
            data=FlavorQuery(name=item.name, uuid=item.uuid), db_items=parent.flavors
        )
        return super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )
