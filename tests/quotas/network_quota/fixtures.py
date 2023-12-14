"""NetworkQuota specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import NetworkQuotaCreateExtended
from app.quota.crud import network_quota_mng
from app.quota.models import NetworkQuota
from app.quota.schemas import (
    NetworkQuotaBase,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    NetworkQuotaUpdate,
    QuotaBase,
)
from app.quota.schemas_extended import (
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
)
from app.region.models import Region
from app.service.models import NetworkService
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

invalid_create_key_values = {
    ("description", None),
    ("per_user", None),
    ("public_ips", -2),  # -1 is valid
    ("networks", -2),  # -1 is valid
    ("ports", -2),  # -1 is valid
    ("security_groups", -2),  # -1 is valid
    ("security_group_rules", -2),  # -1 is valid
}
patch_key_values = {
    ("description", random_lower_string()),
    ("per_user", random_bool()),
    ("public_ips", random_non_negative_int()),
    ("public_ips", -1),
    ("networks", random_non_negative_int()),
    ("networks", -1),
    ("ports", random_non_negative_int()),
    ("ports", -1),
    ("security_groups", random_non_negative_int()),
    ("security_groups", -1),
    ("security_group_rules", random_non_negative_int()),
    ("security_group_rules", -1),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("per_user", None),
    ("public_ips", -2),  # -1 is valid
    ("networks", -2),  # -1 is valid
    ("ports", -2),  # -1 is valid
    ("security_groups", -2),  # -1 is valid
    ("security_group_rules", -2),  # -1 is valid
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def network_quota_create_validator() -> (
    CreateSchemaValidation[NetworkQuotaBase, QuotaBase, NetworkQuotaCreateExtended]
):
    """Instance to validate network_quota create schemas."""
    return CreateSchemaValidation[
        NetworkQuotaBase, QuotaBase, NetworkQuotaCreateExtended
    ](
        base=NetworkQuotaBase,
        base_public=QuotaBase,
        create=NetworkQuotaCreateExtended,
    )


@fixture(scope="package")
def network_quota_read_validator() -> (
    ReadSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
        NetworkQuota,
    ]
):
    """Instance to validate network_quota read schemas."""
    return ReadSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
        NetworkQuota,
    ](
        base=NetworkQuotaBase,
        base_public=QuotaBase,
        read=NetworkQuotaRead,
        read_extended=NetworkQuotaReadExtended,
    )


@fixture(scope="package")
def network_quota_patch_validator() -> (
    BaseSchemaValidation[NetworkQuotaBase, QuotaBase]
):
    """Instance to validate network_quota patch schemas."""
    return BaseSchemaValidation[NetworkQuotaBase, QuotaBase](
        base=NetworkQuotaBase, base_public=QuotaBase
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        NetworkQuotaRead,
        NetworkQuotaReadExtended,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtendedPublic,
    },
)
def network_quota_read_class(cls) -> Any:
    """NetworkQuota Read schema."""
    return cls


# DICT FIXTURES


@fixture
def network_quota_create_mandatory_data() -> Dict[str, Any]:
    """Dict with NetworkQuota mandatory attributes."""
    return {}


@fixture
def network_quota_create_all_data(
    network_quota_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all NetworkQuota attributes."""
    return {
        **network_quota_create_mandatory_data,
        "description": random_lower_string(),
        "per_user": random_bool(),
        "public_ips": random_non_negative_int(),
        "networks": random_non_negative_int(),
        "ports": random_non_negative_int(),
        "security_groups": random_non_negative_int(),
        "security_group_rules": random_non_negative_int(),
    }


@fixture
def network_quota_create_data_with_rel(
    network_quota_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**network_quota_create_all_data, "project": uuid4()}


@fixture
@parametrize("data", {fixture_ref("network_quota_create_data_with_rel")})
def network_quota_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a NetworkQuota patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_quota_create_invalid_pair(
    network_quota_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**network_quota_create_data_with_rel}
    data[k] = v
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("network_quota_create_mandatory_data"),
        fixture_ref("network_quota_create_invalid_pair"),
    },
)
def network_quota_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a NetworkQuota create schema."""
    return data


@fixture
@parametrize("k, v", patch_key_values)
def network_quota_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a NetworkQuota patch schema."""
    return {k: v}


@fixture
def network_quota_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a NetworkQuota patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("network_quota_patch_valid_data_single_attr"),
        fixture_ref("network_quota_patch_valid_data_for_tags"),
    },
)
def network_quota_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a NetworkQuota patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def network_quota_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a NetworkQuota patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_network_quota_simple(
    owned_projects: int,
    network_quota_create_mandatory_data: Dict[str, Any],
    db_compute_serv2: NetworkService,
) -> NetworkQuota:
    """Fixture with standard DB NetworkQuota.

    The network_quota can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = NetworkQuotaCreateExtended(
        **network_quota_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return network_quota_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_network_quota(
    network_quota_create_mandatory_data: Dict[str, Any],
    db_network_quota_simple: NetworkQuota,
    db_compute_serv3: NetworkService,
) -> NetworkQuota:
    """NetworkQuota shared within multiple services."""
    d = {}
    for k in network_quota_create_mandatory_data.keys():
        d[k] = db_network_quota_simple.__getattribute__(k)
    projects = [i.uuid for i in db_network_quota_simple.projects]
    item = NetworkQuotaCreateExtended(
        **d, is_public=len(projects) == 0, projects=projects
    )
    return network_quota_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_network_quota_simple"),
        fixture_ref("db_shared_network_quota"),
    },
)
def db_network_quota(db_item: NetworkQuota) -> NetworkQuota:
    """Generic DB NetworkQuota instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def network_quota_valid_create_schema_tuple(
    network_quota_create_validator, network_quota_create_valid_data
) -> Tuple[
    Type[NetworkQuotaCreateExtended],
    CreateSchemaValidation[NetworkQuotaBase, QuotaBase, NetworkQuotaCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        NetworkQuotaCreateExtended,
        network_quota_create_validator,
        network_quota_create_valid_data,
    )


@fixture
def network_quota_invalid_create_schema_tuple(
    network_quota_create_invalid_data,
) -> Tuple[Type[NetworkQuotaCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkQuotaCreateExtended, network_quota_create_invalid_data


@fixture
def network_quota_valid_patch_schema_tuple(
    network_quota_patch_validator, network_quota_patch_valid_data
) -> Tuple[
    Type[NetworkQuotaUpdate],
    BaseSchemaValidation[NetworkQuotaBase, QuotaBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        NetworkQuotaUpdate,
        network_quota_patch_validator,
        network_quota_patch_valid_data,
    )


@fixture
def network_quota_invalid_patch_schema_tuple(
    network_quota_patch_invalid_data,
) -> Tuple[Type[NetworkQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkQuotaUpdate, network_quota_patch_invalid_data


@fixture
def network_quota_valid_read_schema_tuple(
    network_quota_read_class,
    network_quota_read_validator,
    db_network_quota,
) -> Tuple[
    Union[
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
    ],
    ReadSchemaValidation[
        NetworkQuotaBase,
        QuotaBase,
        NetworkQuotaRead,
        NetworkQuotaReadPublic,
        NetworkQuotaReadExtended,
        NetworkQuotaReadExtendedPublic,
        NetworkQuota,
    ],
    NetworkQuota,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        network_quota_read_class,
        network_quota_read_validator,
        db_network_quota,
    )
