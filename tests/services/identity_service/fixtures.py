"""IdentityService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, fixture_ref, parametrize

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
from tests.utils.block_storage_service import random_block_storage_service_name
from tests.utils.compute_service import random_compute_service_name
from tests.utils.identity_service import random_identity_service_name
from tests.utils.network_service import random_network_service_name
from tests.utils.utils import random_lower_string, random_url

invalid_create_key_values = {
    ("description", None),
    ("type", None),
    ("type", ServiceType.BLOCK_STORAGE),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.NETWORK),
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
    ("type", None),
    ("type", ServiceType.BLOCK_STORAGE),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.NETWORK),
    ("name", random_lower_string()),
    ("name", random_block_storage_service_name()),
    ("name", random_compute_service_name()),
    ("name", random_network_service_name()),
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


# DICT FIXTURES CREATE


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
@parametrize("data", {fixture_ref("identity_service_create_invalid_pair")})
def identity_service_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a IdentityService create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def identity_service_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a IdentityService patch schema."""
    return {k: v}


@fixture
@parametrize("data", {fixture_ref("identity_service_patch_valid_data_single_attr")})
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
def db_identity_service_simple(
    identity_service_create_mandatory_data: Dict[str, Any], db_region_simple: Region
) -> IdentityService:
    """Fixture with standard DB IdentityService."""
    item = IdentityServiceCreate(**identity_service_create_mandatory_data)
    return identity_service_mng.create(obj_in=item, region=db_region_simple)


@fixture
@parametrize("db_item", {fixture_ref("db_identity_service_simple")})
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