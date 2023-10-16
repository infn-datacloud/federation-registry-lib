from typing import List

from app.provider.schemas_extended import UserGroupCreateExtended
from app.tests.utils.sla import create_random_sla, validate_sla_attrs
from app.tests.utils.utils import random_lower_string
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupUpdate


def create_random_user_group(
    *, default: bool = False, projects: List[str] = []
) -> UserGroupCreateExtended:
    name = random_lower_string()
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    if len(projects):
        kwargs["slas"] = [create_random_sla(projects=projects)]
    return UserGroupCreateExtended(name=name, **kwargs)


def create_random_update_user_group_data() -> UserGroupUpdate:
    name = random_lower_string()
    description = random_lower_string()
    return UserGroupUpdate(name=name, description=description)


def validate_user_group_attrs(
    *, obj_in: UserGroupCreateExtended, db_item: UserGroup
) -> None:
    assert db_item.description == db_item.description
    assert db_item.name == obj_in.name
    assert len(db_item.slas) == len(obj_in.slas)
    for db_sla, sla_in in zip(db_item.slas, obj_in.slas):
        validate_sla_attrs(obj_in=sla_in, db_item=db_sla)
