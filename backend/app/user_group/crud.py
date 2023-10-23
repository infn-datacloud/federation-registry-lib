from typing import List, Optional, Union

from app.crud import CRUDBase
from app.identity_provider.models import IdentityProvider
from app.project.models import Project
from app.project.schemas_extended import (
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)
from app.provider.schemas_extended import UserGroupCreateExtended
from app.sla.crud import sla
from app.user_group.models import UserGroup
from app.user_group.schemas import (
    UserGroupCreate,
    UserGroupRead,
    UserGroupReadPublic,
    UserGroupReadShort,
    UserGroupUpdate,
)


class CRUDUserGroup(
    CRUDBase[
        UserGroup,
        UserGroupCreate,
        UserGroupUpdate,
        UserGroupRead,
        UserGroupReadPublic,
        UserGroupReadShort,
        UserGroupReadExtended,
        UserGroupReadExtendedPublic,
    ]
):
    """"""

    def create(
        self,
        *,
        obj_in: UserGroupCreateExtended,
        identity_provider: IdentityProvider,
        projects: List[Project] = []
    ) -> UserGroup:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.identity_provider.connect(identity_provider)
        for db_project in projects:
            if db_project.uuid == obj_in.sla.project:
                db_sla = db_project.sla.single()
                if db_sla is not None:
                    if len(db_sla.projects.all()) == 1:
                        sla.remove(db_obj=db_sla)
                    else:
                        db_project.sla.disconnect(db_sla)
                sla.create(obj_in=obj_in.sla, user_group=db_obj, project=db_project)
        return db_obj

    def remove(self, *, db_obj: UserGroup) -> bool:
        for item in db_obj.slas:
            sla.remove(db_obj=item)
        return super().remove(db_obj=db_obj)

    def update(
        self,
        *,
        db_obj: UserGroup,
        obj_in: Union[UserGroupUpdate, UserGroupCreateExtended],
        projects: List[Project] = [],
        force: bool = False
    ) -> Optional[UserGroup]:
        edit = False
        if force:
            edit = self.__update_slas(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )

        if isinstance(obj_in, UserGroupCreateExtended):
            obj_in = UserGroupUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data

    def __update_slas(
        self,
        *,
        obj_in: UserGroupCreateExtended,
        db_obj: UserGroup,
        provider_projects: List[Project]
    ) -> bool:
        edit = False
        db_items = {db_item.doc_uuid: db_item for db_item in db_obj.slas}
        db_projects = list(
            filter(lambda x: x.uuid in obj_in.sla.project, provider_projects)
        )
        db_project = db_projects[0]
        db_item = db_items.pop(obj_in.sla.doc_uuid, None)
        if not db_item:
            sla.create(obj_in=obj_in.sla, project=db_project, user_group=db_obj)
            edit = True
        else:
            updated_data = sla.update(
                db_obj=db_item, obj_in=obj_in.sla, projects=db_projects, force=True
            )
            if not edit and updated_data is not None:
                edit = True
        # for db_item in db_items.values():
        #     sla.remove(db_obj=db_item)
        #     edit = True
        return edit


user_group = CRUDUserGroup(
    model=UserGroup,
    create_schema=UserGroupCreate,
    read_schema=UserGroupRead,
    read_public_schema=UserGroupReadPublic,
    read_short_schema=UserGroupReadShort,
    read_extended_schema=UserGroupReadExtended,
    read_extended_public_schema=UserGroupReadExtendedPublic,
)
