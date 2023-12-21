"""Network specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_network_create_valid_schema_actors(
    network_create_valid_data,
) -> Tuple[
    Type[NetworkCreateExtended],
    CreateSchemaValidation[NetworkBase, NetworkBasePublic, NetworkCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        NetworkBase, NetworkBasePublic, NetworkCreateExtended
    ](base=NetworkBase, base_public=NetworkBasePublic, create=NetworkCreateExtended)

    return NetworkCreateExtended, validator, network_create_valid_data


@case(tags="create_invalid")
def case_network_create_invalid_schema_actors(
    network_create_invalid_data,
) -> Tuple[Type[NetworkCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return NetworkCreateExtended, network_create_invalid_data


@case(tags="patch_valid")
def case_network_patch_valid_schema_actors(
    network_patch_valid_data,
) -> Tuple[
    Type[NetworkUpdate],
    PatchSchemaValidation[NetworkBase, NetworkBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[NetworkBase, NetworkBasePublic](
        base=NetworkBase, base_public=NetworkBasePublic
    )
    return NetworkUpdate, validator, network_patch_valid_data


@case(tags="patch_invalid")
def case_network_patch_invalid_schema_actors(
    network_patch_invalid_data,
) -> Tuple[Type[NetworkUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return NetworkUpdate, network_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[NetworkRead, NetworkReadExtended, NetworkReadPublic, NetworkReadExtendedPublic]
)
def case_network_valid_read_schema_tuple(
    cls: Union[
        NetworkRead, NetworkReadExtended, NetworkReadPublic, NetworkReadExtendedPublic
    ],
    db_network: Network,
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
    bool,
    bool,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
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
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_network, is_public, is_extended
