"""UserGroup specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_user_group_create_valid_schema_actors(
    user_group_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[UserGroupCreateExtended],
    CreateSchemaValidation[UserGroupBase, UserGroupBasePublic, UserGroupCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        UserGroupBase, UserGroupBasePublic, UserGroupCreateExtended
    ](
        base=UserGroupBase,
        base_public=UserGroupBasePublic,
        create=UserGroupCreateExtended,
    )
    return UserGroupCreateExtended, validator, user_group_create_valid_data


@case(tags="create_invalid")
def case_user_group_create_invalid_schema_actors(
    user_group_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[UserGroupCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return UserGroupCreateExtended, user_group_create_invalid_data


@case(tags="patch_valid")
def case_user_group_patch_valid_schema_actors(
    user_group_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[UserGroupUpdate],
    PatchSchemaValidation[UserGroupBase, UserGroupBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[UserGroupBase, UserGroupBasePublic](
        base=UserGroupBase, base_public=UserGroupBasePublic
    )
    return UserGroupUpdate, validator, user_group_patch_valid_data


@case(tags="patch_invalid")
def case_user_group_patch_invalid_schema_actors(
    user_group_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[UserGroupUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return UserGroupUpdate, user_group_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        UserGroupRead,
        UserGroupReadPublic,
        UserGroupReadExtended,
        UserGroupReadExtendedPublic,
    ]
)
def case_user_group_valid_read_schema_tuple(
    cls: Union[
        UserGroupRead,
        UserGroupReadPublic,
        UserGroupReadExtended,
        UserGroupReadExtendedPublic,
    ],
    db_user_group: UserGroup,
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
    validator = ReadSchemaValidation[
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
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_user_group, is_public, is_extended
