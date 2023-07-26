from app.user_group.crud import user_group
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupCreate, UserGroupUpdate
from app.tests.utils.identity_provider import create_random_identity_provider
from app.tests.utils.utils import random_lower_string


def create_random_user_group() -> UserGroup:
    name = random_lower_string()
    description = random_lower_string()
    item_in = UserGroupCreate(name=name, description=description)
    return user_group.create(
        obj_in=item_in, identity_provider=create_random_identity_provider()
    )


def create_random_update_user_group_data() -> UserGroupUpdate:
    name = random_lower_string()
    description = random_lower_string()
    return UserGroupUpdate(name=name, description=description)
