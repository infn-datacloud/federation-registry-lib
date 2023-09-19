from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb.project import ProjectRead
from models.cmdb.sla import SLAQuery, SLARead, SLAWrite
from models.cmdb.user_group import UserGroupRead
from pydantic import AnyHttpUrl


class SLACRUD(BasicCRUD[SLAWrite, SLARead, SLAQuery]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=SLARead,
            write_schema=SLAWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(
        self, *, item: SLAWrite, project: ProjectRead, user_group: UserGroupRead
    ) -> ProjectRead:
        # db_item, idx = self.find_in_list(
        #    data=SLAQuery(**item.dict()), db_items=project.slas
        # )
        # print(db_item)
        db_item = None
        new_data = super().create_or_update(
            item=item,
            db_item=db_item,
            params={
                "project_uid": project.uid,
                "user_group_uid": user_group.uid,
            },
        )
        project.sla = new_data
        return project
