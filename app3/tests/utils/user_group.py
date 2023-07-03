from ..utils.utils import random_lower_string
from ...user_group.crud import user_group
from ...user_group.models import UserGroup
from ...user_group.schemas import UserGroupCreate, UserGroupUpdate


def create_random_user_group() -> UserGroup:
    name = random_lower_string()
    description = random_lower_string()
    item_in = UserGroupCreate(name=name, description=description)
    return user_group.create(obj_in=item_in)


def create_random_update_user_group_data() -> UserGroupUpdate:
    name = random_lower_string()
    description = random_lower_string()
    return UserGroupUpdate(name=name, description=description)
