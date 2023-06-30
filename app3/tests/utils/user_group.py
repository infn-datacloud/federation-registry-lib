from ..utils.utils import random_lower_string
from ...user_group.crud import user_group
from ...user_group.models import UserGroup
from ...user_group.schemas import UserGroupCreate


def create_random_user_group() -> UserGroup:
    name = random_lower_string()
    description = random_lower_string()
    item_in = UserGroupCreate(name=name, description=description)
    return user_group.create(obj_in=item_in)
