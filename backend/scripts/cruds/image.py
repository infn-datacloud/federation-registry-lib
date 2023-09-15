from typing import Dict

from cruds.core import BasicCRUD
from models.cmdb import ImageQuery, ImageRead, ImageWrite, ProviderRead
from pydantic import AnyHttpUrl


class ImageCRUD(BasicCRUD[ImageWrite, ImageRead, ImageQuery]):
    def __init__(
        self,
        get_url: AnyHttpUrl,
        post_url: AnyHttpUrl,
        patch_url: AnyHttpUrl,
        read_headers: Dict[str, str],
        write_headers: Dict[str, str],
    ) -> None:
        super().__init__(
            type="Image",
            read_schema=ImageRead,
            write_schema=ImageWrite,
            get_url=get_url,
            post_url=post_url,
            patch_url=patch_url,
            read_headers=read_headers,
            write_headers=write_headers,
        )

    def create_or_update(self, *, item: ImageWrite, parent: ProviderRead) -> ImageRead:
        db_item = self.find_in_list(
            data=ImageQuery(name=item.name, uuid=item.uuid), db_items=parent.images
        )
        return super().create_or_update(
            item=item, db_item=db_item, parent_uid=parent.uid
        )
