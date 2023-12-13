"""Network specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.network.crud import network_mng
from app.network.models import Network
from app.network.schemas import (
    NetworkBase,
    NetworkBasePublic,
    NetworkRead,
    NetworkReadPublic,
    NetworkUpdate,
)
from app.network.schemas_extended import NetworkReadExtended, NetworkReadExtendedPublic
from app.provider.models import Provider
from app.provider.schemas_extended import NetworkCreateExtended
from app.region.models import Region
from app.service.models import NetworkService
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)

is_shared = {True, False}
invalid_create_key_values = {
    ("description", None),
    ("uuid", None),
    ("name", None),
    ("is_shared", None),
    ("is_router_external", None),
    ("is_default", None),
    ("mtu", 0),
    ("tags", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("uuid", uuid4()),
    ("name", random_lower_string()),
    ("is_router_external", random_bool()),
    ("is_default", random_bool()),
    ("mtu", random_non_negative_int()),
    ("proxy_ip", random_lower_string()),
    ("proxy_user", random_lower_string()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("is_shared", None),
    ("is_router_external", None),
    ("is_default", None),
    ("mtu", 0),
    ("tags", None),
}


# CLASSES FIXTURES


@fixture(scope="package")
def network_create_validator() -> (
    CreateSchemaValidation[NetworkBase, NetworkBasePublic, NetworkCreateExtended]
):
    """Instance to validate network create schemas."""
    return CreateSchemaValidation[
        NetworkBase, NetworkBasePublic, NetworkCreateExtended
    ](base=NetworkBase, base_public=NetworkBasePublic, create=NetworkCreateExtended)


@fixture(scope="package")
def network_read_validator() -> (
    ReadSchemaValidation[
        NetworkBase,
        NetworkBasePublic,
        NetworkRead,
        NetworkReadPublic,
        NetworkReadExtended,
        NetworkReadExtendedPublic,
        Network,
    ]
):
    """Instance to validate network read schemas."""
    return ReadSchemaValidation[
        NetworkBase,
        NetworkBasePublic,
        NetworkRead,
        NetworkReadPublic,
        NetworkReadExtended,
        NetworkReadExtendedPublic,
        Network,
    ](
        base=NetworkBase,
        base_public=NetworkBasePublic,
        read=NetworkRead,
        read_extended=NetworkReadExtended,
    )


@fixture(scope="package")
def network_patch_validator() -> BaseSchemaValidation[NetworkBase, NetworkBasePublic]:
    """Instance to validate network patch schemas."""
    return BaseSchemaValidation[NetworkBase, NetworkBasePublic](
        base=NetworkBase, base_public=NetworkBasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {NetworkRead, NetworkReadExtended, NetworkReadPublic, NetworkReadExtendedPublic},
)
def network_read_class(cls) -> Any:
    """Network Read schema."""
    return cls


# DICT FIXTURES


@fixture
def network_mandatory_data() -> Dict[str, Any]:
    """Dict with Network mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture
@parametrize("is_shared", is_shared)
def network_all_data(
    is_shared: bool, network_mandatory_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with all Network attributes.

    Attribute is_shared has been parametrized.
    """
    return {
        **network_mandatory_data,
        "is_shared": is_shared,
        "description": random_lower_string(),
        "is_router_external": random_bool(),
        "is_default": random_bool(),
        "mtu": random_positive_int(),
        "proxy_ip": random_lower_string(),
        "proxy_user": random_lower_string(),
        "tags": [random_lower_string()],
    }


@fixture
def network_data_with_relationships(network_all_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    data = {**network_all_data}
    if not data["is_shared"]:
        data["project"] = uuid4()
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("network_mandatory_data"),
        fixture_ref("network_data_with_relationships"),
    },
)
def network_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Network patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def network_create_invalid_pair(
    network_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**network_mandatory_data}
    data[k] = v
    return data


@fixture
@parametrize("is_shared", is_shared)
def network_create_invalid_project_conn(
    network_mandatory_data: Dict[str, Any], is_shared: bool
) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If network is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    data = {**network_mandatory_data}
    data["is_shared"] = is_shared
    data["project"] = None if not is_shared else uuid4()
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("network_create_invalid_pair"),
        fixture_ref("network_create_invalid_project_conn"),
    },
)
def network_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a Network create schema."""
    return data


@fixture
@parametrize("k, v", patch_key_values)
def network_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Network patch schema."""
    return {k: v}


@fixture
def network_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a Network patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("network_patch_valid_data_single_attr"),
        fixture_ref("network_patch_valid_data_for_tags"),
    },
)
def network_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Network patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def network_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Network patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("is_shared", is_shared)
def db_network_simple(
    is_shared: bool,
    network_mandatory_data: Dict[str, Any],
    db_network_serv: NetworkService,
) -> Network:
    """Fixture with standard DB Network.

    The network can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_network_serv.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = NetworkCreateExtended(
        **network_mandatory_data,
        is_shared=is_shared,
        project=None if is_shared else projects[0],
    )
    return network_mng.create(obj_in=item, service=db_network_serv)


@fixture
@parametrize("db_item", {fixture_ref("db_network")})
def db_network(db_item: Network) -> Network:
    """Generic DB Network instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def network_valid_create_schema_tuple(
    network_create_validator, network_create_valid_data
) -> Tuple[
    Type[NetworkCreateExtended],
    CreateSchemaValidation[NetworkBase, NetworkBasePublic, NetworkCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return NetworkCreateExtended, network_create_validator, network_create_valid_data


@fixture
def network_invalid_create_schema_tuple(
    network_create_invalid_data,
) -> Tuple[Type[NetworkCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkCreateExtended, network_create_invalid_data


@fixture
def network_valid_patch_schema_tuple(
    network_patch_validator, network_patch_valid_data
) -> Tuple[
    Type[NetworkUpdate],
    BaseSchemaValidation[NetworkBase, NetworkBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return NetworkUpdate, network_patch_validator, network_patch_valid_data


@fixture
def network_invalid_patch_schema_tuple(
    network_patch_invalid_data,
) -> Tuple[Type[NetworkUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkUpdate, network_patch_invalid_data


@fixture
def network_valid_read_schema_tuple(
    network_read_class, network_read_validator, db_network
) -> Tuple[
    Union[
        NetworkRead, NetworkReadPublic, NetworkReadExtended, NetworkReadExtendedPublic
    ],
    ReadSchemaValidation[
        NetworkBase,
        NetworkBasePublic,
        NetworkRead,
        NetworkReadPublic,
        NetworkReadExtended,
        NetworkReadExtendedPublic,
        Network,
    ],
    Network,
]:
    """Fixture with the read class, validator and the db item to read."""
    return network_read_class, network_read_validator, db_network
