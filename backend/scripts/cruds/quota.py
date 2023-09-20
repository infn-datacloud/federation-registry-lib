from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb.project import ProjectRead
from models.cmdb.quota import QuotaQuery, QuotaRead, QuotaWrite
from models.cmdb.service import ServiceRead
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

    def create_or_update(
        self, *, item: QuotaWrite, project: ProjectRead, service: ServiceRead
    ) -> ProjectRead:
        db_item, idx = self.find_in_list(
            data=QuotaQuery(type=item.type, per_user=item.per_user),
            db_items=project.quotas,
        )
        new_data = super().create_or_update(
            item=item,
            db_item=db_item,
            params={
                "project_uid": project.uid,
                "service_uid": service.uid,
            },
        )
        if db_item is None:
            project.quotas.append(new_data)
        else:
            project.quotas[idx] = new_data
        return project
