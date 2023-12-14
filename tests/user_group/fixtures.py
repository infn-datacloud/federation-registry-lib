"""UserGroup specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import UserGroupCreateExtended
from app.region.models import Region
from app.service.models import ComputeService
from app.user_group.crud import user_group_mng
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
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.utils import random_bool, random_lower_string

invalid_create_key_values = {
    ("description", None),
    ("name", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("name", random_lower_string()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
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


@fixture(scope="package")
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


@fixture(scope="package")
def user_group_patch_validator() -> (
    BaseSchemaValidation[UserGroupBase, UserGroupBasePublic]
):
    """Instance to validate user_group patch schemas."""
    return BaseSchemaValidation[UserGroupBase, UserGroupBasePublic](
        base=UserGroupBase, base_public=UserGroupBasePublic
    )


@fixture(scope="package")
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


# DICT FIXTURES


@fixture
def user_group_create_mandatory_data() -> Dict[str, Any]:
    """Dict with UserGroup mandatory attributes."""
    return {"name": random_lower_string()}


@fixture
def user_group_create_all_data(
    user_group_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all UserGroup attributes."""
    return {**user_group_create_mandatory_data, "description": random_lower_string()}


@fixture
def user_group_create_data_with_rel(
    user_group_create_all_data: Dict[str, Any], sla_create_data_with_rel: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**user_group_create_all_data, "sla": sla_create_data_with_rel}


@fixture
@parametrize("data", {fixture_ref("user_group_create_data_with_rel")})
def user_group_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a UserGroup patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def user_group_create_invalid_pair(
    user_group_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**user_group_create_mandatory_data}
    data[k] = v
    return data


@fixture
def user_group_create_invalid_projects_list_size(
    user_group_create_mandatory_data: Dict[str, Any], is_public: bool
) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If user_group is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    data = {**user_group_create_mandatory_data}
    data["is_public"] = is_public
    data["projects"] = None if not is_public else [uuid4()]
    return data


@fixture
def user_group_create_duplicate_projects(
    user_group_create_mandatory_data: Dict[str, Any],
):
    """Invalid case: the project list has duplicate values."""
    project_uuid = uuid4()
    data = {**user_group_create_mandatory_data}
    data["is_public"] = is_public
    data["projects"] = [project_uuid, project_uuid]
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("user_group_create_invalid_pair"),
        fixture_ref("user_group_create_invalid_projects_list_size"),
        fixture_ref("user_group_create_duplicate_projects"),
    },
)
def user_group_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a UserGroup create schema."""
    return data


@fixture
@parametrize("k, v", patch_key_values)
def user_group_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a UserGroup patch schema."""
    return {k: v}


@fixture
def user_group_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a UserGroup patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("user_group_patch_valid_data_single_attr"),
        fixture_ref("user_group_patch_valid_data_for_tags"),
    },
)
def user_group_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a UserGroup patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def user_group_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a UserGroup patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_user_group_simple(
    owned_projects: int,
    user_group_create_mandatory_data: Dict[str, Any],
    db_compute_serv2: ComputeService,
) -> UserGroup:
    """Fixture with standard DB UserGroup.

    The user_group can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = UserGroupCreateExtended(
        **user_group_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return user_group_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_user_group(
    user_group_create_mandatory_data: Dict[str, Any],
    db_user_group_simple: UserGroup,
    db_compute_serv3: ComputeService,
) -> UserGroup:
    """UserGroup shared within multiple services."""
    d = {}
    for k in user_group_create_mandatory_data.keys():
        d[k] = db_user_group_simple.__getattribute__(k)
    projects = [i.uuid for i in db_user_group_simple.projects]
    item = UserGroupCreateExtended(**d, is_public=len(projects) == 0, projects=projects)
    return user_group_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item",
    {fixture_ref("db_user_group_simple"), fixture_ref("db_shared_user_group")},
)
def db_user_group(db_item: UserGroup) -> UserGroup:
    """Generic DB UserGroup instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


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
    BaseSchemaValidation[UserGroupBase, UserGroupBasePublic],
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
