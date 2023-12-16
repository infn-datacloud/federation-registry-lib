"""UserGroup specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.provider.schemas_extended import UserGroupCreateExtended
from app.user_group.models import UserGroup
from app.user_group.schemas import (
    UserGroupBase,
    UserGroupBasePublic,
    UserGroupRead,
    UserGroupReadPublic,
)
from app.user_group.schemas_extended import (
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def user_group_create_validator() -> (
    CreateSchemaValidation[UserGroupBase, UserGroupBasePublic, UserGroupCreateExtended]
):
    """Instance to validate user_group create schemas."""
    return CreateSchemaValidation[
        UserGroupBase, UserGroupBasePublic, UserGroupCreateExtended
    ](
        base=UserGroupBase,
        base_public=UserGroupBasePublic,
        create=UserGroupCreateExtended,
    )


@fixture
def user_group_read_validator() -> (
    ReadSchemaValidation[
        UserGroupBase,
        UserGroupBasePublic,
        UserGroupRead,
        UserGroupReadPublic,
        UserGroupReadExtended,
        UserGroupReadExtendedPublic,
        UserGroup,
    ]
):
    """Instance to validate user_group read schemas."""
    return ReadSchemaValidation[
        UserGroupBase,
        UserGroupBasePublic,
        UserGroupRead,
        UserGroupReadPublic,
        UserGroupReadExtended,
        UserGroupReadExtendedPublic,
        UserGroup,
    ](
        base=UserGroupBase,
        base_public=UserGroupBasePublic,
        read=UserGroupRead,
        read_extended=UserGroupReadExtended,
    )


@fixture
def user_group_patch_validator() -> (
    BaseSchemaValidation[UserGroupBase, UserGroupBasePublic]
):
    """Instance to validate user_group patch schemas."""
    return BaseSchemaValidation[UserGroupBase, UserGroupBasePublic](
        base=UserGroupBase, base_public=UserGroupBasePublic
    )


@fixture
@parametrize(
    "cls",
    {
        UserGroupRead,
        UserGroupReadExtended,
        UserGroupReadPublic,
        UserGroupReadExtendedPublic,
    },
)
def user_group_read_class(cls) -> Any:
    """UserGroup Read schema."""
    return cls
