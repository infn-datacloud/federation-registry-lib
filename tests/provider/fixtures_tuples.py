"""Provider specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.provider.models import Provider
from app.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderRead,
    ProviderReadPublic,
    ProviderUpdate,
)
from app.provider.schemas_extended import (
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def provider_valid_create_schema_tuple(
    provider_create_validator, provider_create_valid_data
) -> Tuple[
    Type[ProviderCreateExtended],
    CreateSchemaValidation[ProviderBase, ProviderBasePublic, ProviderCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return ProviderCreateExtended, provider_create_validator, provider_create_valid_data


@fixture
def provider_invalid_create_schema_tuple(
    provider_create_invalid_data,
) -> Tuple[Type[ProviderCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ProviderCreateExtended, provider_create_invalid_data


@fixture
def provider_valid_patch_schema_tuple(
    provider_patch_validator, provider_patch_valid_data
) -> Tuple[
    Type[ProviderUpdate],
    BaseSchemaValidation[ProviderBase, ProviderBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return ProviderUpdate, provider_patch_validator, provider_patch_valid_data


@fixture
def provider_invalid_patch_schema_tuple(
    provider_patch_invalid_data,
) -> Tuple[Type[ProviderUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ProviderUpdate, provider_patch_invalid_data


@fixture
def provider_valid_read_schema_tuple(
    provider_read_class, provider_read_validator, db_provider
) -> Tuple[
    Union[
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
    ],
    ReadSchemaValidation[
        ProviderBase,
        ProviderBasePublic,
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
        Provider,
    ],
    Provider,
]:
    """Fixture with the read class, validator and the db item to read."""
    return provider_read_class, provider_read_validator, db_provider
