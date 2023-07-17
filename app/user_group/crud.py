from app.user_group.models import UserGroup as UserGroupModel
from app.user_group.schemas import UserGroupCreate, UserGroupUpdate
from app.crud import CRUDBase


class CRUDUserGroup(
    CRUDBase[UserGroupModel, UserGroupCreate, UserGroupUpdate]
):
    """"""


user_group = CRUDUserGroup(UserGroupModel, UserGroupCreate)
