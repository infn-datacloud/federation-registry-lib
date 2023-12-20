"""Provider specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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


@case(tags="create_valid")
def case_provider_create_valid_schema_actors(
    provider_create_valid_data: Dict[str, Any],
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


@case(tags="create_invalid")
def case_provider_create_invalid_schema_actors(
    provider_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[ProviderCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ProviderCreateExtended, provider_create_invalid_data


@case(tags="patch_valid")
def case_provider_patch_valid_schema_actors(
    provider_patch_valid_data: Dict[str, Any],
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


@case(tags="patch_invalid")
def case_provider_patch_invalid_schema_actors(
    provider_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[ProviderUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ProviderUpdate, provider_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[
        ProviderRead,
        ProviderReadExtended,
        ProviderReadPublic,
        ProviderReadExtendedPublic,
    ]
)
def case_provider_valid_read_schema_tuple(
    cls: Union[
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
    ],
    db_provider: Provider,
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
    bool,
    bool,
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
    cls_name = cls.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return cls, validator, db_provider, is_public, is_extended
