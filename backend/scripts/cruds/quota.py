from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb import ProjectRead, QuotaQuery, QuotaRead, QuotaWrite
from pydantic import AnyHttpUrl


class QuotaCRUD(BasicCRUD[QuotaWrite, QuotaRead, QuotaQuery]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=QuotaRead,
            write_schema=QuotaWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(self, *, item: QuotaWrite, parent: ProjectRead) -> QuotaRead:
        db_item = self.find_in_list(
            data=QuotaQuery(name=item.type), db_items=parent.quotas
        )
        return super().create_or_update(
            item=item,
            db_item=db_item,
            params={
                "project_uid": parent.uid,
                "service_uid": item.service,
            },
        )
