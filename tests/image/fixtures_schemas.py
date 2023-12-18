"""Image specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, parametrize

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
@parametrize(
    cls=[ImageRead, ImageReadExtended, ImageReadPublic, ImageReadExtendedPublic]
)
def image_read_class(cls) -> Any:
    """Image Read schema."""
    return cls


@fixture
def image_create_valid_schema_actors(
    image_create_valid_data,
) -> Tuple[
    Type[ImageCreateExtended],
    CreateSchemaValidation[ImageBase, ImageBasePublic, ImageCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    validator = CreateSchemaValidation[ImageBase, ImageBasePublic, ImageCreateExtended](
        base=ImageBase, base_public=ImageBasePublic, create=ImageCreateExtended
    )
    return ImageCreateExtended, validator, image_create_valid_data


@fixture
def image_create_invalid_schema_actors(
    image_create_invalid_data,
) -> Tuple[Type[ImageCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ImageCreateExtended, image_create_invalid_data


@fixture
def image_patch_valid_schema_actors(
    image_patch_valid_data,
) -> Tuple[
    Type[ImageUpdate],
    PatchSchemaValidation[ImageBase, ImageBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    validator = PatchSchemaValidation[ImageBase, ImageBasePublic](
        base=ImageBase, base_public=ImageBasePublic
    )
    return ImageUpdate, validator, image_patch_valid_data


@fixture
def image_patch_invalid_schema_actors(
    image_patch_invalid_data,
) -> Tuple[Type[ImageUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ImageUpdate, image_patch_invalid_data


@fixture
def image_valid_read_schema_tuple(
    image_read_class, db_image
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
    validator = ReadSchemaValidation[
        ImageBase,
        ImageBasePublic,
        ImageRead,
        ImageReadPublic,
        ImageReadExtended,
        ImageReadExtendedPublic,
        Image,
    ](
        base=ImageBase,
        base_public=ImageBasePublic,
        read=ImageRead,
        read_extended=ImageReadExtended,
    )
    return image_read_class, validator, db_image
