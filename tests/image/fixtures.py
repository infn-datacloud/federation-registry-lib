"""Image specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.image.crud import image_mng
from app.image.models import Image
from app.image.schemas import (
    ImageBase,
    ImageBasePublic,
    ImageRead,
    ImageReadPublic,
    ImageUpdate,
)
from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
from app.provider.models import Provider
from app.provider.schemas_extended import ImageCreateExtended
from app.region.models import Region
from app.service.models import ComputeService
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.image import random_os_type
from tests.utils.utils import random_bool, random_lower_string

is_public = {True, False}
invalid_create_key_values = {
    ("description", None),
    ("uuid", None),
    ("name", None),
    ("is_public", None),
    ("cuda_support", None),
    ("gpu_driver", None),
    ("tags", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("uuid", uuid4()),
    ("name", random_lower_string()),
    ("os_type", random_os_type()),
    ("os_distro", random_lower_string()),
    ("os_version", random_lower_string()),
    ("architecture", random_lower_string()),
    ("kernel_id", random_lower_string()),
    ("cuda_support", random_bool()),
    ("gpu_driver", random_bool()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("is_public", None),
    ("cuda_support", None),
    ("gpu_driver", None),
    ("tags", None),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def image_create_validator() -> (
    CreateSchemaValidation[ImageBase, ImageBasePublic, ImageCreateExtended]
):
    """Instance to validate image create schemas."""
    return CreateSchemaValidation[ImageBase, ImageBasePublic, ImageCreateExtended](
        base=ImageBase, base_public=ImageBasePublic, create=ImageCreateExtended
    )


@fixture(scope="package")
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


@fixture(scope="package")
def image_patch_validator() -> BaseSchemaValidation[ImageBase, ImageBasePublic]:
    """Instance to validate image patch schemas."""
    return BaseSchemaValidation[ImageBase, ImageBasePublic](
        base=ImageBase, base_public=ImageBasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {ImageRead, ImageReadExtended, ImageReadPublic, ImageReadExtendedPublic},
)
def image_read_class(cls) -> Any:
    """Image Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def image_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Image mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture
@parametrize("is_public", is_public)
def image_create_all_data(
    is_public: bool, image_create_mandatory_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with all Image attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **image_create_mandatory_data,
        "is_public": is_public,
        "description": random_lower_string(),
        "os_type": random_os_type(),
        "os_distro": random_lower_string(),
        "os_version": random_lower_string(),
        "architecture": random_lower_string(),
        "kernel_id": random_lower_string(),
        "cuda_support": random_bool(),
        "gpu_driver": random_bool(),
        "tags": [random_lower_string()],
    }


@fixture
def image_create_data_with_rel(image_create_all_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    data = {**image_create_all_data}
    if not data["is_public"]:
        data["projects"] = [uuid4()]
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("image_create_mandatory_data"),
        fixture_ref("image_create_data_with_rel"),
    },
)
def image_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def image_create_invalid_pair(
    image_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**image_create_mandatory_data}
    data[k] = v
    return data


@fixture
@parametrize("is_public", is_public)
def image_create_invalid_projects_list_size(
    image_create_mandatory_data: Dict[str, Any], is_public: bool
) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If image is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    data = {**image_create_mandatory_data}
    data["is_public"] = is_public
    data["projects"] = None if not is_public else [uuid4()]
    return data


@fixture
def image_create_duplicate_projects(image_create_mandatory_data: Dict[str, Any]):
    """Invalid case: the project list has duplicate values."""
    project_uuid = uuid4()
    data = {**image_create_mandatory_data}
    data["is_public"] = is_public
    data["projects"] = [project_uuid, project_uuid]
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("image_create_invalid_pair"),
        fixture_ref("image_create_invalid_projects_list_size"),
        fixture_ref("image_create_duplicate_projects"),
    },
)
def image_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a Image create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def image_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Image patch schema."""
    return {k: v}


@fixture
def image_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("image_patch_valid_data_single_attr"),
        fixture_ref("image_patch_valid_data_for_tags"),
    },
)
def image_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def image_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Image patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_image_simple(
    owned_projects: int,
    image_create_mandatory_data: Dict[str, Any],
    db_compute_serv2: ComputeService,
) -> Image:
    """Fixture with standard DB Image.

    The image can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = ImageCreateExtended(
        **image_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return image_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_image(
    image_create_mandatory_data: Dict[str, Any],
    db_image_simple: Image,
    db_compute_serv3: ComputeService,
) -> Image:
    """Image shared within multiple services."""
    d = {}
    for k in image_create_mandatory_data.keys():
        d[k] = db_image_simple.__getattribute__(k)
    projects = [i.uuid for i in db_image_simple.projects]
    item = ImageCreateExtended(**d, is_public=len(projects) == 0, projects=projects)
    return image_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item", {fixture_ref("db_image_simple"), fixture_ref("db_shared_image")}
)
def db_image(db_item: Image) -> Image:
    """Generic DB Image instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


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
    BaseSchemaValidation[ImageBase, ImageBasePublic],
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
