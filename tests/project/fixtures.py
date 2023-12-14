"""Project specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.project.crud import project_mng
from app.project.models import Project
from app.project.schemas import (
    ProjectBase,
    ProjectBasePublic,
    ProjectRead,
    ProjectReadPublic,
    ProjectUpdate,
)
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from app.provider.models import Provider
from app.provider.schemas_extended import ProjectCreate
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.utils import random_lower_string

invalid_create_key_values = {("description", None), ("uuid", None), ("name", None)}
patch_key_values = {
    ("description", random_lower_string()),
    ("uuid", uuid4()),
    ("name", random_lower_string()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None)
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def project_create_validator() -> (
    CreateSchemaValidation[ProjectBase, ProjectBasePublic, ProjectCreate]
):
    """Instance to validate project create schemas."""
    return CreateSchemaValidation[ProjectBase, ProjectBasePublic, ProjectCreate](
        base=ProjectBase, base_public=ProjectBasePublic, create=ProjectCreate
    )


@fixture(scope="package")
def project_read_validator() -> (
    ReadSchemaValidation[
        ProjectBase,
        ProjectBasePublic,
        ProjectRead,
        ProjectReadPublic,
        ProjectReadExtended,
        ProjectReadExtendedPublic,
        Project,
    ]
):
    """Instance to validate project read schemas."""

    class ReadProjectValidaiton(
        ReadSchemaValidation[
            ProjectBase,
            ProjectBasePublic,
            ProjectRead,
            ProjectReadPublic,
            ProjectReadExtended,
            ProjectReadExtendedPublic,
            Project,
        ]
    ):
        def validate_read_attrs(
            self,
            *,
            db_item: Project,
            schema: Union[
                ProjectRead,
                ProjectReadPublic,
                ProjectReadExtended,
                ProjectReadExtendedPublic,
            ],
            public: bool,
            extended: bool,
        ) -> None:
            return super().validate_read_attrs(
                db_item=db_item,
                schema=schema,
                public=public,
                extended=extended,
                exclude_attrs=[
                    "private_images",
                    "private_flavors",
                    "private_networks",
                ],
            )

    return ReadProjectValidaiton(
        base=ProjectBase,
        base_public=ProjectBasePublic,
        read=ProjectRead,
        read_extended=ProjectReadExtended,
    )


@fixture(scope="package")
def project_patch_validator() -> BaseSchemaValidation[ProjectBase, ProjectBasePublic]:
    """Instance to validate project patch schemas."""
    return BaseSchemaValidation[ProjectBase, ProjectBasePublic](
        base=ProjectBase, base_public=ProjectBasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {ProjectRead, ProjectReadExtended, ProjectReadPublic, ProjectReadExtendedPublic},
)
def project_read_class(cls) -> Any:
    """Project Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def project_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Project mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture
def project_create_all_data(
    project_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Project attributes."""
    return {**project_create_mandatory_data, "description": random_lower_string()}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("project_create_mandatory_data"),
        fixture_ref("project_create_all_data"),
    },
)
def project_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Project patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def project_create_invalid_pair(
    project_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**project_create_mandatory_data}
    data[k] = v
    return data


@fixture
@parametrize("data", {fixture_ref("project_create_invalid_pair")})
def project_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a Project create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def project_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Project patch schema."""
    return {k: v}


@fixture
@parametrize("data", {fixture_ref("project_patch_valid_data_single_attr")})
def project_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Project patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def project_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Project patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
def db_project_simple(
    project_create_mandatory_data: Dict[str, Any], db_provider: Provider
) -> Project:
    """Fixture with standard DB Project."""
    item = ProjectCreate(**project_create_mandatory_data)
    return project_mng.create(obj_in=item, provider=db_provider)


# TODO fixture with db items with flavors, images, networks and quotas.


@fixture
@parametrize("db_item", {fixture_ref("db_project_simple")})
def db_project(db_item: Project) -> Project:
    """Generic DB Project instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def project_valid_create_schema_tuple(
    project_create_validator, project_create_valid_data
) -> Tuple[
    Type[ProjectCreate],
    CreateSchemaValidation[ProjectBase, ProjectBasePublic, ProjectCreate],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return ProjectCreate, project_create_validator, project_create_valid_data


@fixture
def project_invalid_create_schema_tuple(
    project_create_invalid_data,
) -> Tuple[Type[ProjectCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ProjectCreate, project_create_invalid_data


@fixture
def project_valid_patch_schema_tuple(
    project_patch_validator, project_patch_valid_data
) -> Tuple[
    Type[ProjectUpdate],
    BaseSchemaValidation[ProjectBase, ProjectBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return ProjectUpdate, project_patch_validator, project_patch_valid_data


@fixture
def project_invalid_patch_schema_tuple(
    project_patch_invalid_data,
) -> Tuple[Type[ProjectUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ProjectUpdate, project_patch_invalid_data


@fixture
def project_valid_read_schema_tuple(
    project_read_class, project_read_validator, db_project
) -> Tuple[
    Union[
        ProjectRead, ProjectReadPublic, ProjectReadExtended, ProjectReadExtendedPublic
    ],
    ReadSchemaValidation[
        ProjectBase,
        ProjectBasePublic,
        ProjectRead,
        ProjectReadPublic,
        ProjectReadExtended,
        ProjectReadExtendedPublic,
        Project,
    ],
    Project,
]:
    """Fixture with the read class, validator and the db item to read."""
    return project_read_class, project_read_validator, db_project
