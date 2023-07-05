from .models import UserGroup as UserGroupModel
from .schemas import UserGroupCreate, UserGroupUpdate
from ..crud import CRUDBase


class CRUDUserGroup(
    CRUDBase[UserGroupModel, UserGroupCreate, UserGroupUpdate]
):
    """"""


user_group = CRUDUserGroup(UserGroupModel, UserGroupCreate)
