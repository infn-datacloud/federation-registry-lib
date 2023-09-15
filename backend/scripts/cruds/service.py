from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb.provider import ProviderRead
from models.cmdb.service import ServiceQuery, ServiceRead, ServiceWrite
from pydantic import AnyHttpUrl


class ServiceCRUD(BasicCRUD[ServiceWrite, ServiceRead, ServiceQuery]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=ServiceRead,
            write_schema=ServiceWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(
        self, *, item: ServiceWrite, parent: ProviderRead
    ) -> ServiceRead:
        db_item = self.find_in_list(
            data=ServiceQuery(name=item.name), db_items=parent.services
        )
        return super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )
