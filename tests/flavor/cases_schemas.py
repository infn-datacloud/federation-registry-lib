"""Flavor specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorBase,
    FlavorBasePublic,
    FlavorRead,
    FlavorReadPublic,
    FlavorUpdate,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.provider.schemas_extended import FlavorCreateExtended
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)
from tests.common.utils import detect_public_extended_details


@case(tags="create_valid")
def case_flavor_create_valid_schema_actors(
    flavor_create_valid_data: Dict[str, Any],
) -> Tuple[
    Type[FlavorCreateExtended],
    CreateSchemaValidation[FlavorBase, FlavorBasePublic, FlavorCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[
        FlavorBase, FlavorBasePublic, FlavorCreateExtended
    ](base=FlavorBase, base_public=FlavorBasePublic, create=FlavorCreateExtended)
    return FlavorCreateExtended, validator, flavor_create_valid_data


@case(tags="create_invalid")
def case_flavor_create_invalid_schema_actors(
    flavor_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[FlavorCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return FlavorCreateExtended, flavor_create_invalid_data


@case(tags="patch_valid")
def case_flavor_patch_valid_schema_actors(
    flavor_patch_valid_data: Dict[str, Any],
) -> Tuple[
    Type[FlavorUpdate],
    PatchSchemaValidation[FlavorBase, FlavorBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[FlavorBase, FlavorBasePublic](
        base=FlavorBase, base_public=FlavorBasePublic
    )
    return FlavorUpdate, validator, flavor_patch_valid_data


@case(tags="patch_invalid")
def case_flavor_patch_invalid_schema_actors(
    flavor_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[FlavorUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return FlavorUpdate, flavor_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[FlavorRead, FlavorReadExtended, FlavorReadPublic, FlavorReadExtendedPublic],
)
def case_flavor_valid_read_schema_tuple(
    cls: [FlavorRead, FlavorReadExtended, FlavorReadPublic, FlavorReadExtendedPublic],
    db_flavor: Flavor,
) -> Tuple[
    Union[FlavorRead, FlavorReadPublic, FlavorReadExtended, FlavorReadExtendedPublic],
    ReadSchemaValidation[
        FlavorBase,
        FlavorBasePublic,
        FlavorRead,
        FlavorReadPublic,
        FlavorReadExtended,
        FlavorReadExtendedPublic,
        Flavor,
    ],
    Flavor,
    bool,
    bool,
]:
    """Fixture with the read class, validator and the db item to read."""
    validator = ReadSchemaValidation[
        FlavorBase,
        FlavorBasePublic,
        FlavorRead,
        FlavorReadPublic,
        FlavorReadExtended,
        FlavorReadExtendedPublic,
        Flavor,
    ](
        base=FlavorBase,
        base_public=FlavorBasePublic,
        read=FlavorRead,
        read_extended=FlavorReadExtended,
    )
    is_public, is_extended = detect_public_extended_details(cls)
    return cls, validator, db_flavor, is_public, is_extended
