"""UserGroup specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

import pytest
from pytest_cases import fixture, fixture_ref, parametrize

from app.identity_provider.models import IdentityProvider
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import SLACreateExtended, UserGroupCreateExtended
from app.sla.models import SLA
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
from tests.utils.utils import random_lower_string, random_start_end_dates

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
relationships_num = {1, 2}


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


# DICT FIXTURES CREATE


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
@parametrize(
    "data",
    {
        fixture_ref("user_group_create_mandatory_data"),
        fixture_ref("user_group_create_invalid_pair"),
    },
)
def user_group_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a UserGroup create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def user_group_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a UserGroup patch schema."""
    return {k: v}


@fixture
@parametrize("data", {fixture_ref("user_group_patch_valid_data_single_attr")})
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
def db_user_group_simple(db_shared_identity_provider: IdentityProvider) -> UserGroup:
    """Fixture with standard DB UserGroup."""
    return db_shared_identity_provider.user_groups.single()


@fixture
def db_user_group_with_multiple_slas(db_user_group_simple: UserGroup) -> UserGroup:
    """Fixture with a UserGroup with multiple SLAs.

    Each SLA belongs to a different Provider.
    """
    db_idp: IdentityProvider = db_user_group_simple.identity_provider.single()
    if len(db_idp.user_groups) > 2:
        pytest.skip(
            "Case with multiple user groups pointing to the same provider not \
                considered."
        )
    [db_user_group1, db_user_group2] = db_idp.user_groups.all()
    db_sla1: SLA = db_user_group1.slas.single()
    db_project1: Project = db_sla1.projects.single()
    db_provider1: Provider = db_project1.provider.single()
    db_project2: Project = db_provider1.projects.get(uuid__ne=db_project1.uuid)

    user_group_dict = db_user_group2.__dict__
    start_date, end_date = random_start_end_dates()
    item = UserGroupCreateExtended(
        **user_group_dict,
        sla=SLACreateExtended(
            doc_uuid=uuid4(),
            start_date=start_date,
            end_date=end_date,
            project=db_project2.uuid,
        ),
    )

    db_item = user_group_mng.update(
        db_obj=db_user_group2,
        obj_in=item,
        projects=db_provider1.projects,
        force=True,
    )
    assert len(db_item.slas) > 1
    return db_item


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_user_group_simple"),
        fixture_ref("db_user_group_with_multiple_slas"),
    },
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
