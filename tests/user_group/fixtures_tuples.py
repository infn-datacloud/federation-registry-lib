"""UserGroup specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.provider.schemas_extended import UserGroupCreateExtended
from app.user_group.models import UserGroup
from app.user_group.schemas import (
    UserGroupBase,
    UserGroupBasePublic,
    UserGroupRead,
    UserGroupReadPublic,
    UserGroupUpdate,
)
from app.user_group.schemas_extended import (
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def user_group_valid_create_schema_tuple(
    user_group_create_validator, user_group_create_valid_data
) -> Tuple[
    Type[UserGroupCreateExtended],
    CreateSchemaValidation[UserGroupBase, UserGroupBasePublic, UserGroupCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        UserGroupCreateExtended,
        user_group_create_validator,
        user_group_create_valid_data,
    )


@fixture
def user_group_invalid_create_schema_tuple(
    user_group_create_invalid_data,
) -> Tuple[Type[UserGroupCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return UserGroupCreateExtended, user_group_create_invalid_data


@fixture
def user_group_valid_patch_schema_tuple(
    user_group_patch_validator, user_group_patch_valid_data
) -> Tuple[
    Type[UserGroupUpdate],
    PatchSchemaValidation[UserGroupBase, UserGroupBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return UserGroupUpdate, user_group_patch_validator, user_group_patch_valid_data


@fixture
def user_group_invalid_patch_schema_tuple(
    user_group_patch_invalid_data,
) -> Tuple[Type[UserGroupUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return UserGroupUpdate, user_group_patch_invalid_data


@fixture
def user_group_valid_read_schema_tuple(
    user_group_read_class, user_group_read_validator, db_user_group
) -> Tuple[
    Union[
        UserGroupRead,
        UserGroupReadPublic,
        UserGroupReadExtended,
        UserGroupReadExtendedPublic,
    ],
    ReadSchemaValidation[
        UserGroupBase,
        UserGroupBasePublic,
        UserGroupRead,
        UserGroupReadPublic,
        UserGroupReadExtended,
        UserGroupReadExtendedPublic,
        UserGroup,
    ],
    UserGroup,
]:
    """Fixture with the read class, validator and the db item to read."""
    return user_group_read_class, user_group_read_validator, db_user_group
