from typing import Dict, List

from cruds.core import BasicCRUD
from models.cmdb.image import ImageQuery, ImageRead, ImageWrite
from models.cmdb.project import ProjectRead
from models.cmdb.service import ComputeServiceRead
from models.config import URLs


class ImageCRUD(BasicCRUD[ImageWrite, ImageRead, ImageQuery]):
    def __init__(
        self,
        *,
        cmdb_urls: URLs,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            read_schema=ImageRead,
            write_schema=ImageWrite,
            read_headers=read_headers,
            write_headers=write_headers,
            url=cmdb_urls.images,
            parent_url=cmdb_urls.services,
            connectable_items=["projects"],
        )

    def synchronize(
        self,
        *,
        items: List[ImageWrite],
        parent: ComputeServiceRead,
        projects: List[ProjectRead],
    ) -> List[ImageRead]:
        updated_items = []
        db_items = {db_item.uuid: db_item for db_item in parent.images}
        for item in items:
            db_item = db_items.pop(item.name, None)
            if db_item is None:
                new_data = self.create(data=item, parent_uid=parent.uid)
            else:
                updated_item = self.update(new_data=item, uid=db_item.uid)
                new_data = db_item if updated_item is None else updated_item
            updated_items.append(new_data)
        for db_item in db_items:
            self.remove(item=db_item)
        db_projects = {p.uuid: p for p in projects}
        for project_uuid in item.projects:
            db_project = db_projects.get(project_uuid)
            if db_project is not None:
                self.connect(uid=db_item.uid, parent_uid=db_project.uid)
        # TODO disconnect flavors from proj if they have no more access to them
        return updated_items
