from app.crud import CRUDBase
from app.sla.crud import sla
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupCreate, UserGroupUpdate


class CRUDUserGroup(CRUDBase[UserGroup, UserGroupCreate, UserGroupUpdate]):
    """"""

    def remove(self, *, db_obj: UserGroup) -> bool:
        for item in db_obj.slas.all():
            sla.remove(item)
        return super().remove(db_obj=db_obj)


user_group = CRUDUserGroup(UserGroup, UserGroupCreate)
