from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb.project import ProjectQuery, ProjectRead, ProjectWrite
from models.cmdb.provider import ProviderRead
from pydantic import AnyHttpUrl


class ProjectCRUD(BasicCRUD[ProjectWrite, ProjectRead, ProjectQuery]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=ProjectRead,
            write_schema=ProjectWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(
        self, *, item: ProjectWrite, parent: ProviderRead
    ) -> ProjectRead:
        db_item, idx = self.find_in_list(
            data=ProjectQuery(name=item.name, uuid=item.uuid),
            db_items=parent.projects,
            exact=False,
        )
        new_data = super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )
        if db_item is None:
            parent.projects.append(new_data)
        else:
            parent.projects[idx] = new_data
        return parent