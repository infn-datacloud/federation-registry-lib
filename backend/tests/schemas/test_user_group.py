from uuid import uuid4

import pytest
from app.user_group.models import UserGroup
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
from tests.utils.user_group import (
    create_random_user_group,
    validate_read_extended_public_user_group_attrs,
    validate_read_extended_user_group_attrs,
    validate_read_public_user_group_attrs,
    validate_read_short_user_group_attrs,
    validate_read_user_group_attrs,
)


def test_create_schema():
    """Create a valid 'Create' Schema."""
    create_random_user_group(project=uuid4())
    create_random_user_group(default=True, project=uuid4())


def test_invalid_create_schema():
    """List all invalid situations for a 'Create' Schema."""
    a = create_random_user_group(project=uuid4())
    with pytest.raises(ValidationError):
        a.name = None
    with pytest.raises(ValidationError):
        a.sla = None


def test_read_schema_with_one_sla(db_user_group: UserGroup):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target user group has one SLA.
    """
    schema = UserGroupRead.from_orm(db_user_group)
    validate_read_user_group_attrs(obj_out=schema, db_item=db_user_group)
    schema = UserGroupReadShort.from_orm(db_user_group)
    validate_read_short_user_group_attrs(obj_out=schema, db_item=db_user_group)
    schema = UserGroupReadPublic.from_orm(db_user_group)
    validate_read_public_user_group_attrs(obj_out=schema, db_item=db_user_group)
    schema = UserGroupReadExtended.from_orm(db_user_group)
    validate_read_extended_user_group_attrs(obj_out=schema, db_item=db_user_group)
    schema = UserGroupReadExtendedPublic.from_orm(db_user_group)
    validate_read_extended_public_user_group_attrs(
        obj_out=schema, db_item=db_user_group
    )


def test_read_schema_with_multiple_slas(db_user_group_with_multiple_slas: UserGroup):
    """Create a valid 'Read' Schema from DB object.

    Apply conversion for this item for all read schemas. No one of them
    should raise errors.

    Target user group has one SLA.
    """
    schema = UserGroupRead.from_orm(db_user_group_with_multiple_slas)
    validate_read_user_group_attrs(
        obj_out=schema, db_item=db_user_group_with_multiple_slas
    )
    schema = UserGroupReadShort.from_orm(db_user_group_with_multiple_slas)
    validate_read_short_user_group_attrs(
        obj_out=schema, db_item=db_user_group_with_multiple_slas
    )
    schema = UserGroupReadPublic.from_orm(db_user_group_with_multiple_slas)
    validate_read_public_user_group_attrs(
        obj_out=schema, db_item=db_user_group_with_multiple_slas
    )
    schema = UserGroupReadExtended.from_orm(db_user_group_with_multiple_slas)
    assert len(schema.slas) > 1
    validate_read_extended_user_group_attrs(
        obj_out=schema, db_item=db_user_group_with_multiple_slas
    )
    schema = UserGroupReadExtendedPublic.from_orm(db_user_group_with_multiple_slas)
    assert len(schema.slas) > 1
    validate_read_extended_public_user_group_attrs(
        obj_out=schema, db_item=db_user_group_with_multiple_slas
    )
