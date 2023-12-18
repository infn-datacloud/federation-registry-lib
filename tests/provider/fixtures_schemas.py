"""Provider specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, parametrize

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
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
@parametrize(
    cls=[
        ProviderRead,
        ProviderReadExtended,
        ProviderReadPublic,
        ProviderReadExtendedPublic,
    ]
)
def provider_read_class(
    cls,
) -> Union[
    ProviderRead,
    ProviderReadPublic,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
]:
    """Provider Read schema."""
    return cls


@fixture
def provider_valid_create_schema_tuple(
    provider_create_valid_data,
) -> Tuple[
    Type[ProviderCreateExtended],
    CreateSchemaValidation[ProviderBase, ProviderBasePublic, ProviderCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        ProviderBase, ProviderBasePublic, ProviderCreateExtended
    ](base=ProviderBase, base_public=ProviderBasePublic, create=ProviderCreateExtended)
    return ProviderCreateExtended, validator, provider_create_valid_data


@fixture
def provider_invalid_create_schema_tuple(
    provider_create_invalid_data,
) -> Tuple[Type[ProviderCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ProviderCreateExtended, provider_create_invalid_data


@fixture
def provider_valid_patch_schema_tuple(
    provider_patch_valid_data,
) -> Tuple[
    Type[ProviderUpdate],
    PatchSchemaValidation[ProviderBase, ProviderBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[ProviderBase, ProviderBasePublic](
        base=ProviderBase, base_public=ProviderBasePublic
    )
    return ProviderUpdate, validator, provider_patch_valid_data


@fixture
def provider_invalid_patch_schema_tuple(
    provider_patch_invalid_data,
) -> Tuple[Type[ProviderUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ProviderUpdate, provider_patch_invalid_data


@fixture
def provider_valid_read_schema_tuple(
    provider_read_class, db_provider
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
    validator = ReadSchemaValidation[
        ProviderBase,
        ProviderBasePublic,
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
        Provider,
    ](
        base=ProviderBase,
        base_public=ProviderBasePublic,
        read=ProviderRead,
        read_extended=ProviderReadExtended,
    )
    return provider_read_class, validator, db_provider
