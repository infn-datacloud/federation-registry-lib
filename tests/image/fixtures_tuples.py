"""Image specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture

from app.image.models import Image
from app.image.schemas import (
    ImageBase,
    ImageBasePublic,
    ImageRead,
    ImageReadPublic,
    ImageUpdate,
)
from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
from app.provider.schemas_extended import ImageCreateExtended
from tests.common.schemas.validators import (
    CreateSchemaValidation,
    PatchSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def image_valid_create_schema_tuple(
    image_create_validator, image_create_valid_data
) -> Tuple[
    Type[ImageCreateExtended],
    CreateSchemaValidation[ImageBase, ImageBasePublic, ImageCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return ImageCreateExtended, image_create_validator, image_create_valid_data


@fixture
def image_invalid_create_schema_tuple(
    image_create_invalid_data,
) -> Tuple[Type[ImageCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ImageCreateExtended, image_create_invalid_data


@fixture
def image_valid_patch_schema_tuple(
    image_patch_validator, image_patch_valid_data
) -> Tuple[
    Type[ImageUpdate],
    PatchSchemaValidation[ImageBase, ImageBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return ImageUpdate, image_patch_validator, image_patch_valid_data


@fixture
def image_invalid_patch_schema_tuple(
    image_patch_invalid_data,
) -> Tuple[Type[ImageUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ImageUpdate, image_patch_invalid_data


@fixture
def image_valid_read_schema_tuple(
    image_read_class, image_read_validator, db_image
) -> Tuple[
    Union[ImageRead, ImageReadPublic, ImageReadExtended, ImageReadExtendedPublic],
    ReadSchemaValidation[
        ImageBase,
        ImageBasePublic,
        ImageRead,
        ImageReadPublic,
        ImageReadExtended,
        ImageReadExtendedPublic,
        Image,
    ],
    Image,
]:
    """Fixture with the read class, validator and the db item to read."""
    return image_read_class, image_read_validator, db_image
