"""Network specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.network.models import Network
from app.network.schemas import (
    NetworkBase,
    NetworkBasePublic,
    NetworkRead,
    NetworkReadPublic,
    NetworkUpdate,
)
from app.network.schemas_extended import NetworkReadExtended, NetworkReadExtendedPublic
from app.provider.schemas_extended import NetworkCreateExtended
from tests.common.schema_validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


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
    PatchSchemaValidation[NetworkBase, NetworkBasePublic],
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
