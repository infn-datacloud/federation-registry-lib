from typing import List, Optional, Union

from app.crud import CRUDBase
from app.image.models import Image
from app.image.schemas import (
    ImageCreate,
    ImageRead,
    ImageReadPublic,
    ImageReadShort,
    ImageUpdate,
)
from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
from app.project.models import Project
from app.provider.schemas_extended import ImageCreateExtended
from app.service.models import ComputeService


class CRUDImage(
    CRUDBase[
        Image,
        ImageCreate,
        ImageUpdate,
        ImageRead,
        ImageReadPublic,
        ImageReadShort,
        ImageReadExtended,
        ImageReadExtendedPublic,
    ]
):
    """"""

    def create(
        self,
        *,
        obj_in: ImageCreate,
        service: ComputeService,
        projects: List[Project] = []
    ) -> Image:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.services.connect(service)
        for project in projects:
            db_obj.projects.connect(project)
        return db_obj

    def update(
        self,
        *,
        db_obj: Image,
        obj_in: Union[ImageCreateExtended, ImageUpdate],
        projects: List[Project] = [],
        force: bool = False
    ) -> Optional[Image]:
        edit = False
        if force:
            db_items = {db_item.uuid: db_item for db_item in db_obj.projects}
            db_projects = {db_item.uuid: db_item for db_item in projects}
            for proj in obj_in.projects:
                db_item = db_items.pop(proj, None)
                if not db_item:
                    db_item = db_projects.get(proj)
                    db_obj.projects.connect(db_item)
                    edit = True
            for db_item in db_items.values():
                db_obj.projects.disconnect(db_item)
                edit = True

        updated_data = super().update(
            db_obj=db_obj, obj_in=ImageUpdate.parse_obj(obj_in), force=force
        )
        return db_obj if edit else updated_data


image = CRUDImage(
    model=Image,
    create_schema=ImageCreate,
    read_schema=ImageRead,
    read_public_schema=ImageReadPublic,
    read_short_schema=ImageReadShort,
    read_extended_schema=ImageReadExtended,
    read_extended_public_schema=ImageReadExtendedPublic,
)
