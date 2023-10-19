from uuid import uuid4

import pytest
from app.identity_provider.models import IdentityProvider
from app.tests.utils.user_group import create_random_user_group
from app.user_group.crud import user_group
from app.user_group.schemas import (
    UserGroupRead,
    UserGroupReadPublic,
    UserGroupReadShort,
)
from app.user_group.schemas_extended import (
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)
from pydantic import ValidationError


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_user_group()
    create_random_user_group(default=True)
    create_random_user_group(projects=[uuid4()])
    create_random_user_group(default=True, projects=[uuid4()])


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_user_group(projects=[uuid4()])
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        # Duplicated SLAs
        a.slas = [a.slas[0], a.slas[0]]


def test_read_schema(db_idp: IdentityProvider):
    """Create a valid 'Read' Schema."""
    obj_in = create_random_user_group()
    db_obj = user_group.create(obj_in=obj_in, identity_provider=db_idp)
    UserGroupRead.from_orm(db_obj)
    UserGroupReadPublic.from_orm(db_obj)
    UserGroupReadShort.from_orm(db_obj)
    UserGroupReadExtended.from_orm(db_obj)
    UserGroupReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_user_group(default=True)
    db_obj = user_group.create(obj_in=obj_in, identity_provider=db_idp)
    UserGroupRead.from_orm(db_obj)
    UserGroupReadPublic.from_orm(db_obj)
    UserGroupReadShort.from_orm(db_obj)
    UserGroupReadExtended.from_orm(db_obj)
    UserGroupReadExtendedPublic.from_orm(db_obj)

    db_provider = db_idp.providers.all()[0]
    obj_in = create_random_user_group(projects=[i.uuid for i in db_provider.projects])
    db_obj = user_group.create(obj_in=obj_in, identity_provider=db_idp)
    UserGroupRead.from_orm(db_obj)
    UserGroupReadPublic.from_orm(db_obj)
    UserGroupReadShort.from_orm(db_obj)
    UserGroupReadExtended.from_orm(db_obj)
    UserGroupReadExtendedPublic.from_orm(db_obj)

    obj_in = create_random_user_group(
        default=True, projects=[i.uuid for i in db_provider.projects]
    )
    db_obj = user_group.create(obj_in=obj_in, identity_provider=db_idp)
    UserGroupRead.from_orm(db_obj)
    UserGroupReadPublic.from_orm(db_obj)
    UserGroupReadShort.from_orm(db_obj)
    UserGroupReadExtended.from_orm(db_obj)
    UserGroupReadExtendedPublic.from_orm(db_obj)
