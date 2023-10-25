from typing import List, Optional, Union

from app.crud import CRUDBase
from app.project.models import Project
from app.provider.schemas_extended import SLACreateExtended
from app.sla.models import SLA
from app.sla.schemas import SLACreate, SLARead, SLAReadPublic, SLAReadShort, SLAUpdate
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from app.user_group.models import UserGroup


class CRUDSLA(
    CRUDBase[
        SLA,
        SLACreate,
        SLAUpdate,
        SLARead,
        SLAReadPublic,
        SLAReadShort,
        SLAReadExtended,
        SLAReadExtendedPublic,
    ]
):
    """"""

    def create(
        self, *, obj_in: SLACreate, project: Project, user_group: UserGroup
    ) -> SLA:
        db_obj = super().create(obj_in=obj_in)
        db_obj.user_group.connect(user_group)
        db_obj.projects.connect(project)
        return db_obj

    def update(
        self,
        *,
        db_obj: SLA,
        obj_in: Union[SLAUpdate, SLACreateExtended],
        projects: List[Project] = [],
        force: bool = False,
    ) -> Optional[SLA]:
        edit = False
        if force:
            provider_projects = {db_item.uuid: db_item for db_item in projects}
            old_projects_same_provider = list(
                filter(lambda x: x in db_obj.projects, projects)
            )
            db_project = provider_projects.get(obj_in.project)
            if len(old_projects_same_provider) == 0:
                db_obj.projects.connect(db_project)
                edit = True
            else:
                old_project = old_projects_same_provider[0]
                if old_project.uuid != obj_in.project:
                    db_obj.projects.reconnect(old_project, db_project)
                    edit = True

        if isinstance(obj_in, SLACreateExtended):
            obj_in = SLAUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data

    def __update_projects(
        self,
        *,
        obj_in: SLACreateExtended,
        db_obj: SLA,
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


sla = CRUDSLA(
    model=SLA,
    create_schema=SLACreate,
    read_schema=SLARead,
    read_public_schema=SLAReadPublic,
    read_short_schema=SLAReadShort,
    read_extended_schema=SLAReadExtended,
    read_extended_public_schema=SLAReadExtendedPublic,
)
