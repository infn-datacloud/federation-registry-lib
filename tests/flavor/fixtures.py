"""Flavor specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

import pytest
from pytest_cases import fixture, fixture_ref, parametrize

from app.flavor.crud import flavor_mng
from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorBase,
    FlavorBasePublic,
    FlavorRead,
    FlavorReadPublic,
    FlavorUpdate,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.provider.models import Provider
from app.provider.schemas_extended import FlavorCreateExtended
from app.region.models import Region
from app.service.models import ComputeService
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.flavor.controller import FlavorController
from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)


@pytest.fixture(scope="package")
def flavor_controller() -> FlavorController:
    return FlavorController(
        base_schema=FlavorBase,
        base_public_schema=FlavorBase,
        create_schema=FlavorCreateExtended,
        update_schema=FlavorUpdate,
        crud=flavor_mng,
        endpoint_group="flavors",
        item_name="Flavor",
    )


is_public = {True, False}
gpu_details = {
    ("gpu_model", random_lower_string()),  # gpus is 0
    ("gpu_vendor", random_lower_string()),  # gpus is 0
}
invalid_create_key_values = {
    ("uuid", None),
    ("name", None),
    ("is_public", None),
    ("disk", -1),
    ("ram", -1),
    ("vcpus", -1),
    ("swap", -1),
    ("ephemeral", -1),
} | gpu_details
patch_key_values = {
    ("uuid", uuid4()),
    ("name", random_lower_string()),
    ("description", random_lower_string()),
    ("disk", random_non_negative_int()),
    ("ram", random_non_negative_int()),
    ("vcpus", random_non_negative_int()),
    ("swap", random_non_negative_int()),
    ("ephemeral", random_non_negative_int()),
    ("infiniband", random_bool()),
    ("gpus", random_positive_int()),
    ("local_storage", random_lower_string()),
    ("uuid", None),
    ("name", None),
    ("local_storage", None),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("is_public", None),
    ("disk", None),
    ("ram", None),
    ("vcpus", None),
    ("swap", None),
    ("ephemeral", None),
    ("infiniband", None),
    ("gpus", None),
} | gpu_details
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def flavor_create_validator() -> (
    CreateSchemaValidation[FlavorBase, FlavorBasePublic, FlavorCreateExtended]
):
    """Instance to validate flavor create schemas."""
    return CreateSchemaValidation[FlavorBase, FlavorBasePublic, FlavorCreateExtended](
        base=FlavorBase, base_public=FlavorBasePublic, create=FlavorCreateExtended
    )


@fixture(scope="package")
def flavor_read_validator() -> (
    ReadSchemaValidation[
        FlavorBase,
        FlavorBasePublic,
        FlavorRead,
        FlavorReadPublic,
        FlavorReadExtended,
        FlavorReadExtendedPublic,
        Flavor,
    ]
):
    """Instance to validate flavor read schemas."""
    return ReadSchemaValidation[
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


@fixture(scope="package")
def flavor_patch_validator() -> BaseSchemaValidation[FlavorBase, FlavorBasePublic]:
    """Instance to validate flavor patch schemas."""
    return BaseSchemaValidation[FlavorBase, FlavorBasePublic](
        base=FlavorBase, base_public=FlavorBasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {FlavorRead, FlavorReadExtended, FlavorReadPublic, FlavorReadExtendedPublic},
)
def flavor_read_class(cls) -> Any:
    """Flavor Read schema."""
    return cls


# DICT FIXTURES


@fixture
def flavor_mandatory_data() -> Dict[str, Any]:
    """Dict with Flavor mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture
@parametrize("is_public", is_public)
def flavor_all_data(
    is_public: bool, flavor_mandatory_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with all Flavor attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **flavor_mandatory_data,
        "is_public": is_public,
        "description": random_lower_string(),
        "disk": random_non_negative_int(),
        "ram": random_non_negative_int(),
        "vcpus": random_non_negative_int(),
        "swap": random_non_negative_int(),
        "ephemeral": random_non_negative_int(),
        "infiniband": random_bool(),
        "gpus": random_positive_int(),
        "gpu_model": random_lower_string(),
        "gpu_vendor": random_lower_string(),
        "local_storage": random_lower_string(),
    }


@fixture
def flavor_data_with_relationships(flavor_all_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    data = {**flavor_all_data}
    if not data["is_public"]:
        data["projects"] = [uuid4()]
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("flavor_mandatory_data"),
        fixture_ref("flavor_data_with_relationships"),
    },
)
def flavor_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Flavor patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def flavor_create_invalid_pair(
    flavor_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**flavor_mandatory_data}
    data[k] = v
    return data


@fixture
@parametrize("is_public", is_public)
def flavor_create_invalid_projects_list_size(
    flavor_mandatory_data: Dict[str, Any], is_public: bool
) -> Dict[str, Any]:
    """Invalid project list size.

    Invalid cases: If flavor is marked as public, the list has at least one element,
    if private, the list has no items.
    """
    data = {**flavor_mandatory_data}
    data["is_public"] = is_public
    data["projects"] = None if not is_public else [uuid4()]
    return data


@fixture
def flavor_create_duplicate_projects(flavor_mandatory_data: Dict[str, Any]):
    """Invalid case: the project list has duplicate values."""
    project_uuid = uuid4()
    data = {**flavor_mandatory_data}
    data["is_public"] = is_public
    data["projects"] = [project_uuid, project_uuid]
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("flavor_create_invalid_pair"),
        fixture_ref("flavor_create_invalid_projects_list_size"),
        fixture_ref("flavor_create_duplicate_projects"),
    },
)
def flavor_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a Flavor create schema."""
    return data


@fixture
@parametrize("k, v", patch_key_values)
def flavor_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Flavor patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", gpu_details)
def flavor_patch_valid_data_for_gpus(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of attributes for a Flavor patch schema. GPU details."""
    return {"gpus": random_positive_int(), k: v}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("flavor_patch_valid_data_single_attr"),
        fixture_ref("flavor_patch_valid_data_for_gpus"),
    },
)
def flavor_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Flavor patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def flavor_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Flavor patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_flavor_simple(
    owned_projects: int,
    flavor_mandatory_data: Dict[str, Any],
    db_compute_serv2: ComputeService,
) -> Flavor:
    """Fixture with standard DB Flavor.

    The flavor can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = FlavorCreateExtended(
        **flavor_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return flavor_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_flavor(
    flavor_mandatory_data: Dict[str, Any],
    db_flavor: Flavor,
    db_compute_serv3: ComputeService,
) -> Flavor:
    """Flavor shared within multiple services."""
    d = {}
    for k in flavor_mandatory_data.keys():
        d[k] = db_flavor.__getattribute__(k)
    projects = [i.uuid for i in db_flavor.projects]
    item = FlavorCreateExtended(**d, is_public=len(projects) == 0, projects=projects)
    return flavor_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize("db_item", {fixture_ref("db_flavor"), fixture_ref("db_shared_flavor")})
def db_flavor(db_item: Flavor) -> Flavor:
    """Generic DB Flavor instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


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
    BaseSchemaValidation[FlavorBase, FlavorBasePublic],
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
