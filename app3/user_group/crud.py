from .models import UserGroup as UserGroupModel
from .schemas import UserGroupCreate, UserGroupPatch
from ..crud import CRUDBase


class CRUDUserGroup(CRUDBase[UserGroupModel, UserGroupCreate, UserGroupPatch]):
    """"""


user_group = CRUDUserGroup(UserGroupModel, UserGroupCreate)
