"""IdentityProvider specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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


@case(tags="create_valid")
def case_identity_provider_create_valid_schema_actors(
    identity_provider_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[IdentityProviderCreateExtended],
    CreateSchemaValidation[
        IdentityProviderBase, IdentityProviderBasePublic, IdentityProviderCreateExtended
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        IdentityProviderBase, IdentityProviderBasePublic, IdentityProviderCreateExtended
    ](
        base=IdentityProviderBase,
        base_public=IdentityProviderBasePublic,
        create=IdentityProviderCreateExtended,
    )
    return (
        IdentityProviderCreateExtended,
        validator,
        identity_provider_create_valid_data,
    )


@case(tags="create_invalid")
def case_identity_provider_create_invalid_schema_actors(
    identity_provider_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[IdentityProviderCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return IdentityProviderCreateExtended, identity_provider_create_invalid_data


@case(tags="patch_valid")
def case_identity_provider_patch_valid_schema_actors(
    identity_provider_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[IdentityProviderUpdate],
    PatchSchemaValidation[IdentityProviderBase, IdentityProviderBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[IdentityProviderBase, IdentityProviderBasePublic](
        base=IdentityProviderBase, base_public=IdentityProviderBasePublic
    )
    return (
        IdentityProviderUpdate,
        validator,
        identity_provider_patch_valid_data,
    )


@case(tags="patch_invalid")
def case_identity_provider_patch_invalid_schema_actors(
    identity_provider_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[IdentityProviderUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return IdentityProviderUpdate, identity_provider_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        IdentityProviderRead,
        IdentityProviderReadExtended,
        IdentityProviderReadPublic,
        IdentityProviderReadExtendedPublic,
    ],
)
def case_identity_provider_valid_read_schema_tuple(
    cls: [
        IdentityProviderRead,
        IdentityProviderReadExtended,
        IdentityProviderReadPublic,
        IdentityProviderReadExtendedPublic,
    ],
    db_identity_provider: IdentityProvider,
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
    bool,
    bool,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
        IdentityProviderBase,
        IdentityProviderBasePublic,
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
        IdentityProvider,
    ](
        base=IdentityProviderBase,
        base_public=IdentityProviderBasePublic,
        read=IdentityProviderRead,
        read_extended=IdentityProviderReadExtended,
    )
    cls_name = cls.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return cls, validator, db_identity_provider, is_public, is_extended
