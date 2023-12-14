"""NetworkService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import (
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
    NetworkServiceCreateExtended,
)
from app.region.models import Region
from app.service.crud import network_service_mng
from app.service.enum import ServiceType
from app.service.models import NetworkService
from app.service.schemas import (
    NetworkServiceBase,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    NetworkServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
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
    ("type", ServiceType.IDENTITY),
    ("endpoint", None),
    ("name", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("endpoint", random_url()),
    ("name", random_network_service_name()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("type", None),
    ("type", ServiceType.BLOCK_STORAGE),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("name", random_lower_string()),
    ("name", random_block_storage_service_name()),
    ("name", random_compute_service_name()),
    ("name", random_identity_service_name()),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def network_service_create_validator() -> (
    CreateSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceCreateExtended,
    ]
):
    """Instance to validate network_service create schemas."""
    return CreateSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceCreateExtended,
    ](
        base=NetworkServiceBase,
        base_public=ServiceBase,
        create=NetworkServiceCreateExtended,
    )


@fixture(scope="package")
def network_service_read_validator() -> (
    ReadSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
        NetworkService,
    ]
):
    """Instance to validate network_service read schemas."""
    return ReadSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
        NetworkService,
    ](
        base=NetworkServiceBase,
        base_public=ServiceBase,
        read=NetworkServiceRead,
        read_extended=NetworkServiceReadExtended,
    )


@fixture(scope="package")
def network_service_patch_validator() -> (
    BaseSchemaValidation[NetworkServiceBase, ServiceBase]
):
    """Instance to validate network_service patch schemas."""
    return BaseSchemaValidation[NetworkServiceBase, ServiceBase](
        base=NetworkServiceBase, base_public=ServiceBase
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        NetworkServiceRead,
        NetworkServiceReadExtended,
        NetworkServiceReadPublic,
        NetworkServiceReadExtendedPublic,
    },
)
def network_service_read_class(cls) -> Any:
    """NetworkService Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def network_service_create_mandatory_data() -> Dict[str, Any]:
    """Dict with NetworkService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_network_service_name()}


@fixture
def network_service_create_all_data(
    network_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all NetworkService attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **network_service_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
def network_service_create_data_with_networks(
    network_service_create_all_data: Dict[str, Any],
    network_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    network = NetworkCreateExtended(**network_create_data_with_rel)
    return {**network_service_create_all_data, "networks": [network]}


@fixture
def network_service_create_data_with_quotas(
    network_service_create_all_data: Dict[str, Any],
    network_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    return {**network_service_create_all_data, "quotas": [quota]}


@fixture
def network_service_create_data_with_2_quotas_same_proj(
    network_service_create_all_data: Dict[str, Any],
    network_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with 2 quotas on same project.

    A quota has the flag 'per_user' equals to True and the other equal to False.
    """
    quota1 = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    network_quota_create_data_with_rel[
        "per_user"
    ] = not network_quota_create_data_with_rel["per_user"]
    quota2 = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    return {**network_service_create_all_data, "quotas": [quota1, quota2]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("network_service_create_mandatory_data"),
        fixture_ref("network_service_create_data_with_networks"),
        fixture_ref("network_service_create_data_with_quotas"),
        fixture_ref("network_service_create_data_with_2_quotas_same_proj"),
    },
)
def network_service_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a NetworkService patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_service_create_invalid_pair(
    network_service_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**network_service_create_mandatory_data}
    data[k] = v
    return data


@fixture
def network_service_invalid_num_quotas_same_project(
    network_service_create_mandatory_data: Dict[str, Any],
    network_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = NetworkQuotaCreateExtended(**network_quota_create_data_with_rel)
    return {**network_service_create_mandatory_data, "quotas": [quota, quota]}


@fixture
def network_service_create_duplicate_networks(
    network_service_create_mandatory_data: Dict[str, Any],
    network_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the network list has duplicate values."""
    network = NetworkCreateExtended(**network_create_mandatory_data)
    return {**network_service_create_mandatory_data, "networks": [network, network]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("network_service_create_invalid_pair"),
        fixture_ref("network_service_invalid_num_quotas_same_project"),
        fixture_ref("network_service_create_duplicate_networks"),
    },
)
def network_service_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a NetworkService create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def network_service_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a NetworkService patch schema."""
    return {k: v}


@fixture
@parametrize("data", {fixture_ref("network_service_patch_valid_data_single_attr")})
def network_service_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a NetworkService patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def network_service_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a NetworkService patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_network_service_simple(
    owned_projects: int,
    network_service_create_mandatory_data: Dict[str, Any],
    # db_compute_serv2: ComputeService,
) -> NetworkService:
    """Fixture with standard DB NetworkService.

    The network_service can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = NetworkServiceCreateExtended(
        **network_service_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return network_service_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_network_service(
    network_service_create_mandatory_data: Dict[str, Any],
    db_network_service_simple: NetworkService,
    # db_compute_serv3: ComputeService,
) -> NetworkService:
    """NetworkService shared within multiple services."""
    d = {}
    for k in network_service_create_mandatory_data.keys():
        d[k] = db_network_service_simple.__getattribute__(k)
    projects = [i.uuid for i in db_network_service_simple.projects]
    item = NetworkServiceCreateExtended(
        **d, is_public=len(projects) == 0, projects=projects
    )
    return network_service_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_network_service_simple"),
        fixture_ref("db_shared_network_service"),
    },
)
def db_network_service(db_item: NetworkService) -> NetworkService:
    """Generic DB NetworkService instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def network_service_valid_create_schema_tuple(
    network_service_create_validator, network_service_create_valid_data
) -> Tuple[
    Type[NetworkServiceCreateExtended],
    CreateSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceCreateExtended,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        NetworkServiceCreateExtended,
        network_service_create_validator,
        network_service_create_valid_data,
    )


@fixture
def network_service_invalid_create_schema_tuple(
    network_service_create_invalid_data,
) -> Tuple[Type[NetworkServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkServiceCreateExtended, network_service_create_invalid_data


@fixture
def network_service_valid_patch_schema_tuple(
    network_service_patch_validator, network_service_patch_valid_data
) -> Tuple[
    Type[NetworkServiceUpdate],
    BaseSchemaValidation[NetworkServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        NetworkServiceUpdate,
        network_service_patch_validator,
        network_service_patch_valid_data,
    )


@fixture
def network_service_invalid_patch_schema_tuple(
    network_service_patch_invalid_data,
) -> Tuple[Type[NetworkServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkServiceUpdate, network_service_patch_invalid_data


@fixture
def network_service_valid_read_schema_tuple(
    network_service_read_class,
    network_service_read_validator,
    db_network_service,
) -> Tuple[
    Union[
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        NetworkServiceBase,
        ServiceBase,
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
        NetworkService,
    ],
    NetworkService,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        network_service_read_class,
        network_service_read_validator,
        db_network_service,
    )
