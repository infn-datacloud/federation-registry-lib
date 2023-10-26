from app.provider.schemas_extended import UserGroupCreateExtended
from app.tests.utils.sla import create_random_sla, validate_create_sla_attrs
from app.tests.utils.utils import random_lower_string
from app.user_group.models import UserGroup
from app.user_group.schemas import (
    UserGroupBase,
    UserGroupRead,
    UserGroupReadPublic,
    UserGroupReadShort,
    UserGroupUpdate,
)
from app.user_group.schemas_extended import (
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)


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


def validate_user_group_attrs(*, obj_in: UserGroupBase, db_item: UserGroup) -> None:
    assert db_item.description == db_item.description
    assert db_item.name == obj_in.name


def validate_user_group_public_attrs(
    *, obj_in: UserGroupBase, db_item: UserGroup
) -> None:
    assert db_item.description == db_item.description
    assert db_item.name == obj_in.name


def validate_create_user_group_attrs(
    *, obj_in: UserGroupCreateExtended, db_item: UserGroup
) -> None:
    validate_user_group_attrs(obj_in=obj_in, db_item=db_item)
    assert len(db_item.slas) > 0
    db_slas = list(filter(lambda x: x.doc_uuid == obj_in.sla.doc_uuid, db_item.slas))
    assert len(db_slas) == 1
    validate_create_sla_attrs(obj_in=obj_in.sla, db_item=db_slas[0])


def validate_read_user_group_attrs(
    *, obj_out: UserGroupRead, db_item: UserGroup
) -> None:
    assert db_item.uid == obj_out.uid
    validate_user_group_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_short_user_group_attrs(
    *, obj_out: UserGroupReadShort, db_item: UserGroup
) -> None:
    assert db_item.uid == obj_out.uid
    validate_user_group_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_public_user_group_attrs(
    *, obj_out: UserGroupReadPublic, db_item: UserGroup
) -> None:
    assert db_item.uid == obj_out.uid
    validate_user_group_public_attrs(obj_in=obj_out, db_item=db_item)


def validate_read_extended_user_group_attrs(
    *, obj_out: UserGroupReadExtended, db_item: UserGroup
) -> None:
    assert db_item.uid == obj_out.uid
    validate_user_group_attrs(obj_in=obj_out, db_item=db_item)
    db_idp = db_item.identity_provider.single()
    assert db_idp
    assert db_idp.uid == obj_out.identity_provider.uid
    assert len(db_item.slas) == len(obj_out.slas)
    for db_sla, sla_out in zip(db_item.slas, obj_out.slas):
        assert db_sla.uid == sla_out.uid


def validate_read_extended_public_user_group_attrs(
    *, obj_out: UserGroupReadExtendedPublic, db_item: UserGroup
) -> None:
    assert db_item.uid == obj_out.uid
    validate_user_group_public_attrs(obj_in=obj_out, db_item=db_item)
    db_idp = db_item.identity_provider.single()
    assert db_idp
    assert db_idp.uid == obj_out.identity_provider.uid
    assert len(db_item.slas) == len(obj_out.slas)
    for db_sla, sla_out in zip(db_item.slas, obj_out.slas):
        assert db_sla.uid == sla_out.uid
