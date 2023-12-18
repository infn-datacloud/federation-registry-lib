"""IdentityProvider specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderBasePublic,
    IdentityProviderRead,
    IdentityProviderReadPublic,
    IdentityProviderUpdate,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
)
from app.provider.schemas_extended import (
    IdentityProviderCreateExtended,
)
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def identity_provider_valid_create_schema_tuple(
    identity_provider_create_validator, identity_provider_create_valid_data
) -> Tuple[
    Type[IdentityProviderCreateExtended],
    CreateSchemaValidation[
        IdentityProviderBase, IdentityProviderBasePublic, IdentityProviderCreateExtended
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        IdentityProviderCreateExtended,
        identity_provider_create_validator,
        identity_provider_create_valid_data,
    )


@fixture
def identity_provider_invalid_create_schema_tuple(
    identity_provider_create_invalid_data,
) -> Tuple[Type[IdentityProviderCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return IdentityProviderCreateExtended, identity_provider_create_invalid_data


@fixture
def identity_provider_valid_patch_schema_tuple(
    identity_provider_patch_validator, identity_provider_patch_valid_data
) -> Tuple[
    Type[IdentityProviderUpdate],
    PatchSchemaValidation[IdentityProviderBase, IdentityProviderBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        IdentityProviderUpdate,
        identity_provider_patch_validator,
        identity_provider_patch_valid_data,
    )


@fixture
def identity_provider_invalid_patch_schema_tuple(
    identity_provider_patch_invalid_data,
) -> Tuple[Type[IdentityProviderUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return IdentityProviderUpdate, identity_provider_patch_invalid_data


@fixture
def identity_provider_valid_read_schema_tuple(
    identity_provider_read_class, identity_provider_read_validator, db_identity_provider
) -> Tuple[
    Union[
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
    ],
    ReadSchemaValidation[
        IdentityProviderBase,
        IdentityProviderBasePublic,
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
        IdentityProvider,
    ],
    IdentityProvider,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        identity_provider_read_class,
        identity_provider_read_validator,
        db_identity_provider,
    )
