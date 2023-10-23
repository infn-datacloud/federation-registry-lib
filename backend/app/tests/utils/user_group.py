from app.provider.schemas_extended import UserGroupCreateExtended
from app.tests.utils.sla import create_random_sla, validate_sla_attrs
from app.tests.utils.utils import random_lower_string
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupUpdate


def create_random_user_group(
    *, default: bool = False, project: str
) -> UserGroupCreateExtended:
    name = random_lower_string()
    sla = create_random_sla(project=project)
    kwargs = {}
    if not default:
        kwargs = {"description": random_lower_string()}
    return UserGroupCreateExtended(name=name, sla=sla, **kwargs)


def create_random_user_group_patch(*, default: bool = False) -> UserGroupUpdate:
    if default:
        return UserGroupUpdate()
    name = random_lower_string()
    description = random_lower_string()
    return UserGroupUpdate(name=name, description=description)


def validate_user_group_attrs(
    *, obj_in: UserGroupCreateExtended, db_item: UserGroup
) -> None:
    assert db_item.description == db_item.description
    assert db_item.name == obj_in.name
    assert len(db_item.slas) > 0
    db_slas = list(filter(lambda x: x.doc_uuid == obj_in.sla.doc_uuid, db_item.slas))
    assert len(db_slas) == 1
    validate_sla_attrs(obj_in=obj_in.sla, db_item=db_slas[0])
