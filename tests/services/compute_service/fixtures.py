"""ComputeService specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import (
    ComputeQuotaCreateExtended,
    ComputeServiceCreateExtended,
    FlavorCreateExtended,
    ImageCreateExtended,
)
from app.region.models import Region
from app.service.crud import compute_service_mng
from app.service.enum import ServiceType
from app.service.models import ComputeService
from app.service.schemas import (
    ComputeServiceBase,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceUpdate,
    ServiceBase,
)
from app.service.schemas_extended import (
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.compute_service import random_compute_service_name
from tests.utils.utils import random_lower_string, random_url

invalid_create_key_values = {
    ("description", None),
    ("endpoint", None),
    ("name", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("endpoint", random_url()),
    ("name", random_compute_service_name()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("type", ServiceType.COMPUTE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def compute_service_create_validator() -> (
    CreateSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceCreateExtended,
    ]
):
    """Instance to validate compute_service create schemas."""
    return CreateSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceCreateExtended,
    ](
        base=ComputeServiceBase,
        base_public=ServiceBase,
        create=ComputeServiceCreateExtended,
    )


@fixture(scope="package")
def compute_service_read_validator() -> (
    ReadSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
        ComputeService,
    ]
):
    """Instance to validate compute_service read schemas."""
    return ReadSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
        ComputeService,
    ](
        base=ComputeServiceBase,
        base_public=ServiceBase,
        read=ComputeServiceRead,
        read_extended=ComputeServiceReadExtended,
    )


@fixture(scope="package")
def compute_service_patch_validator() -> (
    BaseSchemaValidation[ComputeServiceBase, ServiceBase]
):
    """Instance to validate compute_service patch schemas."""
    return BaseSchemaValidation[ComputeServiceBase, ServiceBase](
        base=ComputeServiceBase, base_public=ServiceBase
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        ComputeServiceRead,
        ComputeServiceReadExtended,
        ComputeServiceReadPublic,
        ComputeServiceReadExtendedPublic,
    },
)
def compute_service_read_class(cls) -> Any:
    """ComputeService Read schema."""
    return cls


# DICT FIXTURES


@fixture
def compute_service_create_mandatory_data() -> Dict[str, Any]:
    """Dict with ComputeService mandatory attributes."""
    return {"endpoint": random_url(), "name": random_compute_service_name()}


@fixture
def compute_service_create_all_data(
    compute_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all ComputeService attributes."""
    return {
        **compute_service_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
def compute_service_create_data_with_flavors(
    compute_service_create_all_data: Dict[str, Any],
    flavor_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    flavor = FlavorCreateExtended(**flavor_create_data_with_rel)
    return {**compute_service_create_all_data, "flavors": [flavor]}


@fixture
def compute_service_create_data_with_images(
    compute_service_create_all_data: Dict[str, Any],
    image_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    image = ImageCreateExtended(**image_create_data_with_rel)
    return {**compute_service_create_all_data, "images": [image]}


@fixture
def compute_service_create_data_with_quotas(
    compute_service_create_all_data: Dict[str, Any],
    compute_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = ComputeQuotaCreateExtended(**compute_quota_create_data_with_rel)
    return {**compute_service_create_all_data, "quotas": [quota]}


@fixture
def compute_service_create_data_with_2_quotas_same_proj(
    compute_service_create_all_data: Dict[str, Any],
    compute_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with 2 quotas on same project.

    A quota has the flag 'per_user' equals to True and the other equal to False.
    """
    quota1 = ComputeQuotaCreateExtended(**compute_quota_create_data_with_rel)
    compute_quota_create_data_with_rel[
        "per_user"
    ] = not compute_quota_create_data_with_rel["per_user"]
    quota2 = ComputeQuotaCreateExtended(**compute_quota_create_data_with_rel)
    return {**compute_service_create_all_data, "quotas": [quota1, quota2]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("compute_service_create_mandatory_data"),
        fixture_ref("compute_service_create_data_with_flavors"),
        fixture_ref("compute_service_create_data_with_images"),
        fixture_ref("compute_service_create_data_with_quotas"),
        fixture_ref("compute_service_create_data_with_2_quotas_same_proj"),
    },
)
def compute_service_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a ComputeService patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def compute_service_create_invalid_pair(
    compute_service_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**compute_service_create_mandatory_data}
    data[k] = v
    return data


@fixture
def compute_service_invalid_num_quotas_same_project(
    compute_service_create_mandatory_data: Dict[str, Any],
    compute_quota_create_data_with_rel: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = ComputeQuotaCreateExtended(**compute_quota_create_data_with_rel)
    return {**compute_service_create_mandatory_data, "quotas": [quota, quota]}


@fixture
def compute_service_create_duplicate_flavors(
    compute_service_create_mandatory_data: Dict[str, Any],
    flavor_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the flavor list has duplicate values."""
    flavor = FlavorCreateExtended(**flavor_create_mandatory_data)
    return {**compute_service_create_mandatory_data, "flavors": [flavor, flavor]}


@fixture
def compute_service_create_duplicate_images(
    compute_service_create_mandatory_data: Dict[str, Any],
    image_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the image list has duplicate values."""
    image = ImageCreateExtended(**image_create_mandatory_data)
    return {**compute_service_create_mandatory_data, "images": [image, image]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("compute_service_create_invalid_pair"),
        fixture_ref("compute_service_invalid_num_quotas_same_project"),
        fixture_ref("compute_service_create_duplicate_flavors"),
        fixture_ref("compute_service_create_duplicate_images"),
    },
)
def compute_service_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a ComputeService create schema."""
    return data


@fixture
@parametrize("k, v", patch_key_values)
def compute_service_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a ComputeService patch schema."""
    return {k: v}


@fixture
def compute_service_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a ComputeService patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("compute_service_patch_valid_data_single_attr"),
        fixture_ref("compute_service_patch_valid_data_for_tags"),
    },
)
def compute_service_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a ComputeService patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def compute_service_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a ComputeService patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_compute_service_simple(
    owned_projects: int,
    compute_service_create_mandatory_data: Dict[str, Any],
    db_compute_serv2: ComputeService,
) -> ComputeService:
    """Fixture with standard DB ComputeService.

    The compute_service can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = ComputeServiceCreateExtended(
        **compute_service_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return compute_service_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_compute_service(
    compute_service_create_mandatory_data: Dict[str, Any],
    db_compute_service_simple: ComputeService,
    db_compute_serv3: ComputeService,
) -> ComputeService:
    """ComputeService shared within multiple services."""
    d = {}
    for k in compute_service_create_mandatory_data.keys():
        d[k] = db_compute_service_simple.__getattribute__(k)
    projects = [i.uuid for i in db_compute_service_simple.projects]
    item = ComputeServiceCreateExtended(
        **d, is_public=len(projects) == 0, projects=projects
    )
    return compute_service_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_compute_service_simple"),
        fixture_ref("db_shared_compute_service"),
    },
)
def db_compute_service(db_item: ComputeService) -> ComputeService:
    """Generic DB ComputeService instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def compute_service_valid_create_schema_tuple(
    compute_service_create_validator, compute_service_create_valid_data
) -> Tuple[
    Type[ComputeServiceCreateExtended],
    CreateSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceCreateExtended,
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        ComputeServiceCreateExtended,
        compute_service_create_validator,
        compute_service_create_valid_data,
    )


@fixture
def compute_service_invalid_create_schema_tuple(
    compute_service_create_invalid_data,
) -> Tuple[Type[ComputeServiceCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ComputeServiceCreateExtended, compute_service_create_invalid_data


@fixture
def compute_service_valid_patch_schema_tuple(
    compute_service_patch_validator, compute_service_patch_valid_data
) -> Tuple[
    Type[ComputeServiceUpdate],
    BaseSchemaValidation[ComputeServiceBase, ServiceBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        ComputeServiceUpdate,
        compute_service_patch_validator,
        compute_service_patch_valid_data,
    )


@fixture
def compute_service_invalid_patch_schema_tuple(
    compute_service_patch_invalid_data,
) -> Tuple[Type[ComputeServiceUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ComputeServiceUpdate, compute_service_patch_invalid_data


@fixture
def compute_service_valid_read_schema_tuple(
    compute_service_read_class,
    compute_service_read_validator,
    db_compute_service,
) -> Tuple[
    Union[
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
    ],
    ReadSchemaValidation[
        ComputeServiceBase,
        ServiceBase,
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
        ComputeService,
    ],
    ComputeService,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        compute_service_read_class,
        compute_service_read_validator,
        db_compute_service,
    )
