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
from tests.utils.user_group import create_random_user_group


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


def test_read_schema(db_user_group: UserGroup):
    """Create a valid 'Read' Schema."""
    UserGroupRead.from_orm(db_user_group)
    UserGroupReadPublic.from_orm(db_user_group)
    UserGroupReadShort.from_orm(db_user_group)
    UserGroupReadExtended.from_orm(db_user_group)
    UserGroupReadExtendedPublic.from_orm(db_user_group)
