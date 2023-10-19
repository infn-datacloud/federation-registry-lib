from typing import List, Optional, Union

from app.crud import CRUDBase
from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorCreate,
    FlavorRead,
    FlavorReadPublic,
    FlavorReadShort,
    FlavorUpdate,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.project.models import Project
from app.provider.schemas_extended import FlavorCreateExtended
from app.service.models import ComputeService


class CRUDFlavor(
    CRUDBase[
        Flavor,
        FlavorCreate,
        FlavorUpdate,
        FlavorRead,
        FlavorReadPublic,
        FlavorReadShort,
        FlavorReadExtended,
        FlavorReadExtendedPublic,
    ]
):
    """"""

    def create(
        self,
        *,
        obj_in: FlavorCreate,
        service: ComputeService,
        projects: List[Project] = [],
    ) -> Flavor:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.services.connect(service)
        for project in projects:
            db_obj.projects.connect(project)
        return db_obj

    def update(
        self,
        *,
        db_obj: Flavor,
        obj_in: Union[FlavorUpdate, FlavorCreateExtended],
        projects: List[Project] = [],
        force: bool = False,
    ) -> Optional[Flavor]:
        edit = False
        if force:
            edit = self.__update_projects(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )

        if isinstance(obj_in, FlavorCreateExtended):
            obj_in = FlavorUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data

    def __update_projects(
        self,
        *,
        obj_in: FlavorCreateExtended,
        db_obj: Flavor,
        provider_projects: List[Project],
    ) -> bool:
        edit = False
        db_items = {db_item.uuid: db_item for db_item in db_obj.projects}
        db_projects = {db_item.uuid: db_item for db_item in provider_projects}
        for proj in obj_in.projects:
            db_item = db_items.pop(proj, None)
            if not db_item:
                db_item = db_projects.get(proj)
                db_obj.projects.connect(db_item)
                edit = True
        for db_item in db_items.values():
            db_obj.projects.disconnect(db_item)
            edit = True
        return edit


flavor = CRUDFlavor(
    model=Flavor,
    create_schema=FlavorCreate,
    read_schema=FlavorRead,
    read_public_schema=FlavorReadPublic,
    read_short_schema=FlavorReadShort,
    read_extended_schema=FlavorReadExtended,
    read_extended_public_schema=FlavorReadExtendedPublic,
)
