from app.user_group.models import UserGroup 
from app.user_group.schemas import UserGroupCreate, UserGroupUpdate
from app.crud import CRUDBase


class CRUDUserGroup(
    CRUDBase[UserGroup, UserGroupCreate, UserGroupUpdate]
):
    """"""


user_group = CRUDUserGroup(UserGroup, UserGroupCreate)
