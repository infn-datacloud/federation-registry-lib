"""Image specific cases."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import case, parametrize

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


@case(tags="create_valid")
def case_image_create_valid_schema_actors(
    image_create_valid_data: Dict[str, Any],
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


@case(tags="create_invalid")
def case_image_create_invalid_schema_actors(
    image_create_invalid_data: Dict[str, Any],
) -> Tuple[Type[ImageCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ImageCreateExtended, image_create_invalid_data


@case(tags="patch_valid")
def case_image_patch_valid_schema_actors(
    image_patch_valid_data: Dict[str, Any],
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


@case(tags="patch_invalid")
def case_image_patch_invalid_schema_actors(
    image_patch_invalid_data: Dict[str, Any],
) -> Tuple[Type[ImageUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ImageUpdate, image_patch_invalid_data


@case(tags="read")
@parametrize(
    cls=[ImageRead, ImageReadExtended, ImageReadPublic, ImageReadExtendedPublic]
)
def case_image_valid_read_schema_tuple(
    cls: [ImageRead, ImageReadExtended, ImageReadPublic, ImageReadExtendedPublic],
    db_image: Image,
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
    bool,
    bool,
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
    cls_name = cls.__name__
    is_public = False
    is_extended = False
    if "Public" in cls_name:
        is_public = True
    if "Extended" in cls_name:
        is_extended = True
    return cls, validator, db_image, is_public, is_extended
