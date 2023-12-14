"""ComputeQuota specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import ComputeQuotaCreateExtended
from app.quota.crud import compute_quota_mng
from app.quota.enum import QuotaType
from app.quota.models import ComputeQuota
from app.quota.schemas import (
    ComputeQuotaBase,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaUpdate,
    QuotaBase,
)
from app.quota.schemas_extended import (
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from app.region.models import Region
from app.service.models import ComputeService
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int

invalid_create_key_values = {
    ("description", None),
    ("per_user", None),
    ("cores", -1),
    ("instances", -1),
    ("ram", -1),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("per_user", random_bool()),
    ("cores", random_non_negative_int()),
    ("instances", random_non_negative_int()),
    ("ram", random_non_negative_int()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("per_user", None),
    ("type", QuotaType.BLOCK_STORAGE),
    ("type", QuotaType.NETWORK),
    ("cores", -1),
    ("instances", -1),
    ("ram", -1),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def compute_quota_create_validator() -> (
    CreateSchemaValidation[ComputeQuotaBase, QuotaBase, ComputeQuotaCreateExtended]
):
    """Instance to validate compute_quota create schemas."""
    return CreateSchemaValidation[
        ComputeQuotaBase, QuotaBase, ComputeQuotaCreateExtended
    ](
        base=ComputeQuotaBase,
        base_public=QuotaBase,
        create=ComputeQuotaCreateExtended,
    )


@fixture(scope="package")
def compute_quota_read_validator() -> (
    ReadSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
        ComputeQuota,
    ]
):
    """Instance to validate compute_quota read schemas."""
    return ReadSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
        ComputeQuota,
    ](
        base=ComputeQuotaBase,
        base_public=QuotaBase,
        read=ComputeQuotaRead,
        read_extended=ComputeQuotaReadExtended,
    )


@fixture(scope="package")
def compute_quota_patch_validator() -> (
    BaseSchemaValidation[ComputeQuotaBase, QuotaBase]
):
    """Instance to validate compute_quota patch schemas."""
    return BaseSchemaValidation[ComputeQuotaBase, QuotaBase](
        base=ComputeQuotaBase, base_public=QuotaBase
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        ComputeQuotaRead,
        ComputeQuotaReadExtended,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtendedPublic,
    },
)
def compute_quota_read_class(cls) -> Any:
    """ComputeQuota Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def compute_quota_create_mandatory_data() -> Dict[str, Any]:
    """Dict with ComputeQuota mandatory attributes."""
    return {}


@fixture
def compute_quota_create_all_data(
    compute_quota_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all ComputeQuota attributes."""
    return {
        **compute_quota_create_mandatory_data,
        "description": random_lower_string(),
        "per_user": random_bool(),
        "cores": random_non_negative_int(),
        "instances": random_non_negative_int(),
        "ram": random_non_negative_int(),
    }


@fixture
def compute_quota_create_data_with_rel(
    compute_quota_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**compute_quota_create_all_data, "project": uuid4()}


@fixture
@parametrize("data", {fixture_ref("compute_quota_create_data_with_rel")})
def compute_quota_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a ComputeQuota patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def compute_quota_create_invalid_pair(
    compute_quota_create_data_with_rel: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**compute_quota_create_data_with_rel}
    data[k] = v
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("compute_quota_create_mandatory_data"),
        fixture_ref("compute_quota_create_invalid_pair"),
    },
)
def compute_quota_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a ComputeQuota create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def compute_quota_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a ComputeQuota patch schema."""
    return {k: v}


@fixture
@parametrize("data", {fixture_ref("compute_quota_patch_valid_data_single_attr")})
def compute_quota_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a ComputeQuota patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def compute_quota_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a ComputeQuota patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_compute_quota_simple(
    owned_projects: int,
    compute_quota_create_mandatory_data: Dict[str, Any],
    db_compute_serv2: ComputeService,
) -> ComputeQuota:
    """Fixture with standard DB ComputeQuota.

    The compute_quota can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = ComputeQuotaCreateExtended(
        **compute_quota_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return compute_quota_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_compute_quota(
    compute_quota_create_mandatory_data: Dict[str, Any],
    db_compute_quota_simple: ComputeQuota,
    db_compute_serv3: ComputeService,
) -> ComputeQuota:
    """ComputeQuota shared within multiple services."""
    d = {}
    for k in compute_quota_create_mandatory_data.keys():
        d[k] = db_compute_quota_simple.__getattribute__(k)
    projects = [i.uuid for i in db_compute_quota_simple.projects]
    item = ComputeQuotaCreateExtended(
        **d, is_public=len(projects) == 0, projects=projects
    )
    return compute_quota_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_compute_quota_simple"),
        fixture_ref("db_shared_compute_quota"),
    },
)
def db_compute_quota(db_item: ComputeQuota) -> ComputeQuota:
    """Generic DB ComputeQuota instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def compute_quota_valid_create_schema_tuple(
    compute_quota_create_validator, compute_quota_create_valid_data
) -> Tuple[
    Type[ComputeQuotaCreateExtended],
    CreateSchemaValidation[ComputeQuotaBase, QuotaBase, ComputeQuotaCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        ComputeQuotaCreateExtended,
        compute_quota_create_validator,
        compute_quota_create_valid_data,
    )


@fixture
def compute_quota_invalid_create_schema_tuple(
    compute_quota_create_invalid_data,
) -> Tuple[Type[ComputeQuotaCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ComputeQuotaCreateExtended, compute_quota_create_invalid_data


@fixture
def compute_quota_valid_patch_schema_tuple(
    compute_quota_patch_validator, compute_quota_patch_valid_data
) -> Tuple[
    Type[ComputeQuotaUpdate],
    BaseSchemaValidation[ComputeQuotaBase, QuotaBase],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        ComputeQuotaUpdate,
        compute_quota_patch_validator,
        compute_quota_patch_valid_data,
    )


@fixture
def compute_quota_invalid_patch_schema_tuple(
    compute_quota_patch_invalid_data,
) -> Tuple[Type[ComputeQuotaUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ComputeQuotaUpdate, compute_quota_patch_invalid_data


@fixture
def compute_quota_valid_read_schema_tuple(
    compute_quota_read_class,
    compute_quota_read_validator,
    db_compute_quota,
) -> Tuple[
    Union[
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
    ],
    ReadSchemaValidation[
        ComputeQuotaBase,
        QuotaBase,
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
        ComputeQuota,
    ],
    ComputeQuota,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        compute_quota_read_class,
        compute_quota_read_validator,
        db_compute_quota,
    )
