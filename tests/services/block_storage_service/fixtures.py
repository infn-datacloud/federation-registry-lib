"""BlockStorageService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    BlockStorageServiceCreateExtended,
)
from app.region.models import Region
from app.service.crud import block_storage_service_mng
from app.service.enum import ServiceType
from app.service.models import BlockStorageService
from app.service.schemas import (
    BlockStorageServiceBase,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    BlockStorageServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
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
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
    ("endpoint", None),
    ("name", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("endpoint", random_url()),
    ("name", random_block_storage_service_name()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("type", None),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
    ("name", random_lower_string()),
    ("name", random_compute_service_name()),
    ("name", random_identity_service_name()),
    ("name", random_network_service_name()),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def block_storage_service_create_validator() -> (
    CreateSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceCreateExtended,
    ]
):
    """Instance to validate block_storage_service create schemas."""
    return CreateSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceCreateExtended,
    ](
        base=BlockStorageServiceBase,
        base_public=ServiceBase,
        create=BlockStorageServiceCreateExtended,
    )


@fixture(scope="package")
def block_storage_service_read_validator() -> (
    ReadSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
        BlockStorageService,
    ]
):
    """Instance to validate block_storage_service read schemas."""
    return ReadSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
        BlockStorageService,
    ](
        base=BlockStorageServiceBase,
        base_public=ServiceBase,
        read=BlockStorageServiceRead,
        read_extended=BlockStorageServiceReadExtended,
    )


@fixture(scope="package")
def block_storage_service_patch_validator() -> (
    BaseSchemaValidation[BlockStorageServiceBase, ServiceBase]
):
    """Instance to validate block_storage_service patch schemas."""
    return BaseSchemaValidation[BlockStorageServiceBase, ServiceBase](
        base=BlockStorageServiceBase, base_public=ServiceBase
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        BlockStorageServiceRead,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtendedPublic,
    },
)
def block_storage_service_read_class(cls) -> Any:
    """BlockStorageService Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def block_storage_service_create_mandatory_data() -> Dict[str, Any]:
    """Dict with BlockStorageService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_block_storage_service_name()}


@fixture
def block_storage_service_create_all_data(
    block_storage_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all BlockStorageService attributes."""
    return {
        **block_storage_service_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
def block_storage_service_create_data_with_rel(
    block_storage_service_create_all_data: Dict[str, Any],
    block_storage_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    return {**block_storage_service_create_all_data, "quotas": [quota]}


@fixture
def block_storage_service_create_data_with_2_quotas_same_proj(
    block_storage_service_create_all_data: Dict[str, Any],
    block_storage_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with 2 quotas on same project.

    A quota has the flag 'per_user' equals to True and the other equal to False.
    """
    quota1 = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    block_storage_quota_create_data_with_rel[
        "per_user"
    ] = not block_storage_quota_create_data_with_rel["per_user"]
    quota2 = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    return {**block_storage_service_create_all_data, "quotas": [quota1, quota2]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("block_storage_service_create_mandatory_data"),
        fixture_ref("block_storage_service_create_data_with_rel"),
        fixture_ref("block_storage_service_create_data_with_2_quotas_same_proj"),
    },
)
def block_storage_service_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a BlockStorageService patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def block_storage_service_create_invalid_pair(
    block_storage_service_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**block_storage_service_create_mandatory_data}
    data[k] = v
    return data


@fixture
def block_storage_service_invalid_num_quotas_same_project(
    block_storage_service_create_mandatory_data: Dict[str, Any],
    block_storage_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = BlockStorageQuotaCreateExtended(**block_storage_quota_create_data_with_rel)
    return {**block_storage_service_create_mandatory_data, "quotas": [quota, quota]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("block_storage_service_create_invalid_pair"),
        fixture_ref("block_storage_service_invalid_num_quotas_same_project"),
    },
)
def block_storage_service_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a BlockStorageService create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def block_storage_service_patch_valid_data_single_attr(
    k: str, v: Any
) -> Dict[str, Any]:
    """Valid set of single key-value pair for a BlockStorageService patch schema."""
    return {k: v}


@fixture
@parametrize(
    "data", {fixture_ref("block_storage_service_patch_valid_data_single_attr")}
)
def block_storage_service_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a BlockStorageService patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def block_storage_service_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a BlockStorageService patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_block_storage_service_simple(
    owned_projects: int,
    block_storage_service_create_mandatory_data: Dict[str, Any],
    # db_compute_serv2: ComputeService,
) -> BlockStorageService:
    """Fixture with standard DB BlockStorageService.

    The block_storage_service can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = BlockStorageServiceCreateExtended(
        **block_storage_service_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return block_storage_service_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_block_storage_service(
    block_storage_service_create_mandatory_data: Dict[str, Any],
    db_block_storage_service_simple: BlockStorageService,
    # db_compute_serv3: ComputeService,
) -> BlockStorageService:
    """BlockStorageService shared within multiple services."""
    d = {}
    for k in block_storage_service_create_mandatory_data.keys():
        d[k] = db_block_storage_service_simple.__getattribute__(k)
    projects = [i.uuid for i in db_block_storage_service_simple.projects]
    item = BlockStorageServiceCreateExtended(
        **d, is_public=len(projects) == 0, projects=projects
    )
    return block_storage_service_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_block_storage_service_simple"),
        fixture_ref("db_shared_block_storage_service"),
    },
)
def db_block_storage_service(db_item: BlockStorageService) -> BlockStorageService:
    """Generic DB BlockStorageService instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def block_storage_service_valid_create_schema_tuple(
    block_storage_service_create_validator, block_storage_service_create_valid_data
) -> Tuple[
    Type[BlockStorageServiceCreateExtended],
    CreateSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceCreateExtended,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        BlockStorageServiceCreateExtended,
        block_storage_service_create_validator,
        block_storage_service_create_valid_data,
    )


@fixture
def block_storage_service_invalid_create_schema_tuple(
    block_storage_service_create_invalid_data,
) -> Tuple[Type[BlockStorageServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return BlockStorageServiceCreateExtended, block_storage_service_create_invalid_data


@fixture
def block_storage_service_valid_patch_schema_tuple(
    block_storage_service_patch_validator, block_storage_service_patch_valid_data
) -> Tuple[
    Type[BlockStorageServiceUpdate],
    BaseSchemaValidation[BlockStorageServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        BlockStorageServiceUpdate,
        block_storage_service_patch_validator,
        block_storage_service_patch_valid_data,
    )


@fixture
def block_storage_service_invalid_patch_schema_tuple(
    block_storage_service_patch_invalid_data,
) -> Tuple[Type[BlockStorageServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return BlockStorageServiceUpdate, block_storage_service_patch_invalid_data


@fixture
def block_storage_service_valid_read_schema_tuple(
    block_storage_service_read_class,
    block_storage_service_read_validator,
    db_block_storage_service,
) -> Tuple[
    Union[
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        BlockStorageServiceBase,
        ServiceBase,
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
        BlockStorageService,
    ],
    BlockStorageService,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        block_storage_service_read_class,
        block_storage_service_read_validator,
        db_block_storage_service,
    )
