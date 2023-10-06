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
        projects: List[Project]
    ) -> UserGroup:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.identity_provider.connect(identity_provider)
        for item in obj_in.slas:
            item_projects = [str(i) for i in item.projects]
            db_projects = list(filter(lambda x: x.uuid in item_projects, projects))
            if len(db_projects) > 0:
                sla.create(obj_in=item, user_group=db_obj, projects=db_projects)
        return db_obj

    def remove(self, *, db_obj: UserGroup) -> bool:
        for item in db_obj.slas:
            sla.remove(db_obj=item)
        return super().remove(db_obj=db_obj)

    def update(
        self,
        *,
        db_obj: UserGroup,
        obj_in: Union[UserGroupCreateExtended, UserGroupUpdate],
        projects: List[Project] = [],
        force: bool = False
    ) -> Optional[UserGroup]:
        if force:
            db_items = {db_item.doc_uuid: db_item for db_item in db_obj.slas}
            for item in obj_in.slas:
                db_item = db_items.pop(str(item.doc_uuid), None)
                item_projects = [str(i) for i in item.projects]
                db_projects = list(filter(lambda x: x.uuid in item_projects, projects))
                if db_item is None:
                    sla.create(obj_in=item, projects=db_projects, user_group=db_obj)
                else:
                    sla.update(
                        db_obj=db_item, obj_in=item, projects=db_projects, force=force
                    )
            for db_item in db_items.values():
                sla.remove(db_obj=db_item)
        return super().update(db_obj=db_obj, obj_in=obj_in, force=force)


user_group = CRUDUserGroup(
    model=UserGroup,
    create_schema=UserGroupCreate,
    read_schema=UserGroupRead,
    read_public_schema=UserGroupReadPublic,
    read_short_schema=UserGroupReadShort,
    read_extended_schema=UserGroupReadExtended,
    read_extended_public_schema=UserGroupReadExtendedPublic,
)
