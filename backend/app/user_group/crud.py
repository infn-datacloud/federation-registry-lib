from app.crud import CRUDBase
from app.identity_provider.models import IdentityProvider
from app.sla.crud import sla
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupCreate, UserGroupUpdate


class CRUDUserGroup(CRUDBase[UserGroup, UserGroupCreate, UserGroupUpdate]):
    """"""

    def create(
        self,
        *,
        obj_in: UserGroupCreate,
        identity_provider: IdentityProvider,
        force: bool = False
    ) -> UserGroup:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.identity_provider.connect(identity_provider)
        return db_obj

    def remove(self, *, db_obj: UserGroup) -> bool:
        for item in db_obj.slas.all():
            sla.remove(item)
        return super().remove(db_obj=db_obj)


user_group = CRUDUserGroup(UserGroup, UserGroupCreate)
