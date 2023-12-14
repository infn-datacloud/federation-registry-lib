"""IdentityService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import IdentityServiceCreate
from app.region.models import Region
from app.service.crud import identity_service_mng
from app.service.enum import ServiceType
from app.service.models import IdentityService
from app.service.schemas import (
    IdentityServiceBase,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.identity_service import random_identity_service_name
from tests.utils.utils import random_lower_string, random_url

invalid_create_key_values = {
    ("description", None),
    ("endpoint", None),
    ("name", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("endpoint", random_url()),
    ("name", random_identity_service_name()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def identity_service_create_validator() -> (
    CreateSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceCreate,
    ]
):
    """Instance to validate identity_service create schemas."""
    return CreateSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceCreate,
    ](
        base=IdentityServiceBase,
        base_public=ServiceBase,
        create=IdentityServiceCreate,
    )


@fixture(scope="package")
def identity_service_read_validator() -> (
    ReadSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
        IdentityService,
    ]
):
    """Instance to validate identity_service read schemas."""
    return ReadSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
        IdentityService,
    ](
        base=IdentityServiceBase,
        base_public=ServiceBase,
        read=IdentityServiceRead,
        read_extended=IdentityServiceReadExtended,
    )


@fixture(scope="package")
def identity_service_patch_validator() -> (
    BaseSchemaValidation[IdentityServiceBase, ServiceBase]
):
    """Instance to validate identity_service patch schemas."""
    return BaseSchemaValidation[IdentityServiceBase, ServiceBase](
        base=IdentityServiceBase, base_public=ServiceBase
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        IdentityServiceRead,
        IdentityServiceReadExtended,
        IdentityServiceReadPublic,
        IdentityServiceReadExtendedPublic,
    },
)
def identity_service_read_class(cls) -> Any:
    """IdentityService Read schema."""
    return cls


# DICT FIXTURES


@fixture
def identity_service_create_mandatory_data() -> Dict[str, Any]:
    """Dict with IdentityService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_identity_service_name()}


@fixture
def identity_service_create_all_data(
    identity_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all IdentityService attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **identity_service_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
@parametrize("data", {fixture_ref("identity_service_create_mandatory_data")})
def identity_service_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a IdentityService patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def identity_service_create_invalid_pair(
    identity_service_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**identity_service_create_mandatory_data}
    data[k] = v
    return data


@fixture
def identity_service_create_invalid_projects_list_size(
    identity_service_create_mandatory_data: Dict[str, Any], is_public: bool
) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If identity_service is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    data = {**identity_service_create_mandatory_data}
    data["is_public"] = is_public
    data["projects"] = None if not is_public else [uuid4()]
    return data


@fixture
def identity_service_create_duplicate_projects(
    identity_service_create_mandatory_data: Dict[str, Any],
):
    """Invalid case: the project list has duplicate values."""
    project_uuid = uuid4()
    data = {**identity_service_create_mandatory_data}
    data["is_public"] = is_public
    data["projects"] = [project_uuid, project_uuid]
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("identity_service_create_invalid_pair"),
        fixture_ref("identity_service_create_invalid_projects_list_size"),
        fixture_ref("identity_service_create_duplicate_projects"),
    },
)
def identity_service_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a IdentityService create schema."""
    return data


@fixture
@parametrize("k, v", patch_key_values)
def identity_service_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a IdentityService patch schema."""
    return {k: v}


@fixture
def identity_service_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a IdentityService patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("identity_service_patch_valid_data_single_attr"),
        fixture_ref("identity_service_patch_valid_data_for_tags"),
    },
)
def identity_service_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a IdentityService patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def identity_service_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a IdentityService patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_identity_service_simple(
    owned_projects: int,
    identity_service_create_mandatory_data: Dict[str, Any],
    # db_compute_serv2: ComputeService,
) -> IdentityService:
    """Fixture with standard DB IdentityService.

    The identity_service can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = IdentityServiceCreate(
        **identity_service_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return identity_service_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_identity_service(
    identity_service_create_mandatory_data: Dict[str, Any],
    db_identity_service_simple: IdentityService,
    # db_compute_serv3: ComputeService,
) -> IdentityService:
    """IdentityService shared within multiple services."""
    d = {}
    for k in identity_service_create_mandatory_data.keys():
        d[k] = db_identity_service_simple.__getattribute__(k)
    projects = [i.uuid for i in db_identity_service_simple.projects]
    item = IdentityServiceCreate(**d, is_public=len(projects) == 0, projects=projects)
    return identity_service_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_identity_service_simple"),
        fixture_ref("db_shared_identity_service"),
    },
)
def db_identity_service(db_item: IdentityService) -> IdentityService:
    """Generic DB IdentityService instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def identity_service_valid_create_schema_tuple(
    identity_service_create_validator, identity_service_create_valid_data
) -> Tuple[
    Type[IdentityServiceCreate],
    CreateSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceCreate,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        IdentityServiceCreate,
        identity_service_create_validator,
        identity_service_create_valid_data,
    )


@fixture
def identity_service_invalid_create_schema_tuple(
    identity_service_create_invalid_data,
) -> Tuple[Type[IdentityServiceCreate], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return IdentityServiceCreate, identity_service_create_invalid_data


@fixture
def identity_service_valid_patch_schema_tuple(
    identity_service_patch_validator, identity_service_patch_valid_data
) -> Tuple[
    Type[IdentityServiceUpdate],
    BaseSchemaValidation[IdentityServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        IdentityServiceUpdate,
        identity_service_patch_validator,
        identity_service_patch_valid_data,
    )


@fixture
def identity_service_invalid_patch_schema_tuple(
    identity_service_patch_invalid_data,
) -> Tuple[Type[IdentityServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return IdentityServiceUpdate, identity_service_patch_invalid_data


@fixture
def identity_service_valid_read_schema_tuple(
    identity_service_read_class,
    identity_service_read_validator,
    db_identity_service,
) -> Tuple[
    Union[
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        IdentityServiceBase,
        ServiceBase,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
        IdentityService,
    ],
    IdentityService,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        identity_service_read_class,
        identity_service_read_validator,
        db_identity_service,
    )
