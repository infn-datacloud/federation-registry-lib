"""Network specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.network.models import Network
from app.network.schemas import (
    NetworkBase,
    NetworkBasePublic,
    NetworkRead,
    NetworkReadPublic,
)
from app.network.schemas_extended import NetworkReadExtended, NetworkReadExtendedPublic
from app.provider.schemas_extended import NetworkCreateExtended
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def network_create_validator() -> (
    CreateSchemaValidation[NetworkBase, NetworkBasePublic, NetworkCreateExtended]
):
    """Instance to validate network create schemas."""
    return CreateSchemaValidation[
        NetworkBase, NetworkBasePublic, NetworkCreateExtended
    ](base=NetworkBase, base_public=NetworkBasePublic, create=NetworkCreateExtended)


@fixture
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


@fixture
def network_patch_validator() -> BaseSchemaValidation[NetworkBase, NetworkBasePublic]:
    """Instance to validate network patch schemas."""
    return BaseSchemaValidation[NetworkBase, NetworkBasePublic](
        base=NetworkBase, base_public=NetworkBasePublic
    )


@fixture
@parametrize(
    "cls",
    {NetworkRead, NetworkReadExtended, NetworkReadPublic, NetworkReadExtendedPublic},
)
def network_read_class(cls) -> Any:
    """Network Read schema."""
    return cls
