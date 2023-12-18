"""Flavor specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

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


@fixture
def flavor_valid_create_schema_tuple(
    flavor_create_validator, flavor_create_valid_data
) -> Tuple[
    Type[FlavorCreateExtended],
    CreateSchemaValidation[FlavorBase, FlavorBasePublic, FlavorCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return FlavorCreateExtended, flavor_create_validator, flavor_create_valid_data


@fixture
def flavor_invalid_create_schema_tuple(
    flavor_create_invalid_data,
) -> Tuple[Type[FlavorCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return FlavorCreateExtended, flavor_create_invalid_data


@fixture
def flavor_valid_patch_schema_tuple(
    flavor_patch_validator, flavor_patch_valid_data
) -> Tuple[
    Type[FlavorUpdate],
    PatchSchemaValidation[FlavorBase, FlavorBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return FlavorUpdate, flavor_patch_validator, flavor_patch_valid_data


@fixture
def flavor_invalid_patch_schema_tuple(
    flavor_patch_invalid_data,
) -> Tuple[Type[FlavorUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return FlavorUpdate, flavor_patch_invalid_data


@fixture
def flavor_valid_read_schema_tuple(
    flavor_read_class, flavor_read_validator, db_flavor
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
]:
    """Fixture with the read class, validator and the db item to read."""
    return flavor_read_class, flavor_read_validator, db_flavor
