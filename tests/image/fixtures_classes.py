"""Image specific fixtures."""
from typing import Any

from pytest_cases import fixture, parametrize

from app.image.models import Image
from app.image.schemas import (
    ImageBase,
    ImageBasePublic,
    ImageRead,
    ImageReadPublic,
)
from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
from app.provider.schemas_extended import ImageCreateExtended
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


@fixture
def image_create_validator() -> (
    CreateSchemaValidation[ImageBase, ImageBasePublic, ImageCreateExtended]
):
    """Instance to validate image create schemas."""
    return CreateSchemaValidation[ImageBase, ImageBasePublic, ImageCreateExtended](
        base=ImageBase, base_public=ImageBasePublic, create=ImageCreateExtended
    )


@fixture
def image_read_validator() -> (
    ReadSchemaValidation[
        ImageBase,
        ImageBasePublic,
        ImageRead,
        ImageReadPublic,
        ImageReadExtended,
        ImageReadExtendedPublic,
        Image,
    ]
):
    """Instance to validate image read schemas."""
    return ReadSchemaValidation[
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


@fixture
def image_patch_validator() -> BaseSchemaValidation[ImageBase, ImageBasePublic]:
    """Instance to validate image patch schemas."""
    return BaseSchemaValidation[ImageBase, ImageBasePublic](
        base=ImageBase, base_public=ImageBasePublic
    )


@fixture
@parametrize(
    cls=[ImageRead, ImageReadExtended, ImageReadPublic, ImageReadExtendedPublic]
)
def image_read_class(cls) -> Any:
    """Image Read schema."""
    return cls
