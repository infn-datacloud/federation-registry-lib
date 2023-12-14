"""Region specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    IdentityServiceCreate,
    LocationCreate,
    NetworkServiceCreateExtended,
    RegionCreateExtended,
)
from app.region.crud import region_mng
from app.region.models import Region
from app.region.schemas import (
    RegionBase,
    RegionBasePublic,
    RegionRead,
    RegionReadPublic,
    RegionUpdate,
)
from app.region.schemas_extended import RegionReadExtended, RegionReadExtendedPublic
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.block_storage_service import random_block_storage_service_name
from tests.utils.compute_service import random_compute_service_name
from tests.utils.identity_service import random_identity_service_name
from tests.utils.network_service import random_network_service_name
from tests.utils.utils import random_lower_string, random_url

invalid_create_key_values = {("description", None), ("name", None)}
patch_key_values = {
    ("description", random_lower_string()),
    ("name", random_lower_string()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None)
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def region_create_validator() -> (
    CreateSchemaValidation[RegionBase, RegionBasePublic, RegionCreateExtended]
):
    """Instance to validate region create schemas."""
    return CreateSchemaValidation[RegionBase, RegionBasePublic, RegionCreateExtended](
        base=RegionBase, base_public=RegionBasePublic, create=RegionCreateExtended
    )


@fixture(scope="package")
def region_read_validator() -> (
    ReadSchemaValidation[
        RegionBase,
        RegionBasePublic,
        RegionRead,
        RegionReadPublic,
        RegionReadExtended,
        RegionReadExtendedPublic,
        Region,
    ]
):
    """Instance to validate region read schemas."""
    return ReadSchemaValidation[
        RegionBase,
        RegionBasePublic,
        RegionRead,
        RegionReadPublic,
        RegionReadExtended,
        RegionReadExtendedPublic,
        Region,
    ](
        base=RegionBase,
        base_public=RegionBasePublic,
        read=RegionRead,
        read_extended=RegionReadExtended,
    )


@fixture(scope="package")
def region_patch_validator() -> BaseSchemaValidation[RegionBase, RegionBasePublic]:
    """Instance to validate region patch schemas."""
    return BaseSchemaValidation[RegionBase, RegionBasePublic](
        base=RegionBase, base_public=RegionBasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {RegionRead, RegionReadExtended, RegionReadPublic, RegionReadExtendedPublic},
)
def region_read_class(cls) -> Any:
    """Region Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def region_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Region mandatory attributes."""
    return {"name": random_lower_string()}


@fixture
def region_create_all_data(
    region_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with Region mandatory attributes."""
    return {**region_create_mandatory_data, "description": random_lower_string()}


@fixture
def region_create_data_with_location(
    region_create_all_data: Dict[str, Any],
    location_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    location = LocationCreate(**location_create_mandatory_data)
    return {**region_create_all_data, "location": location}


@fixture
@parametrize(owned_services=relationships_num)
def region_create_data_with_block_storage_services(
    owned_services: int,
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    services = []
    for _ in range(owned_services):
        services.append(
            BlockStorageServiceCreateExtended(
                endpoint=random_url(), name=random_block_storage_service_name()
            )
        )
    return {**region_create_all_data, "block_storage_services": services}


@fixture
@parametrize(owned_services=relationships_num)
def region_create_data_with_compute_services(
    owned_services: int,
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    services = []
    for _ in range(owned_services):
        services.append(
            ComputeServiceCreateExtended(
                endpoint=random_url(), name=random_compute_service_name()
            )
        )
    return {**region_create_all_data, "compute_services": services}


@fixture
@parametrize(owned_services=relationships_num)
def region_create_data_with_identity_services(
    owned_services: int,
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    services = []
    for _ in range(owned_services):
        services.append(
            IdentityServiceCreate(
                endpoint=random_url(), name=random_identity_service_name()
            )
        )
    return {**region_create_all_data, "identity_services": services}


@fixture
@parametrize(owned_services=relationships_num)
def region_create_data_with_network_services(
    owned_services: int,
    region_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    services = []
    for _ in range(owned_services):
        services.append(
            NetworkServiceCreateExtended(
                endpoint=random_url(), name=random_network_service_name()
            )
        )
    return {**region_create_all_data, "network_services": services}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("region_create_mandatory_data"),
        fixture_ref("region_create_data_with_location"),
        fixture_ref("region_create_data_with_block_storage_services"),
        fixture_ref("region_create_data_with_compute_services"),
        fixture_ref("region_create_data_with_identity_services"),
        fixture_ref("region_create_data_with_network_services"),
    },
)
def region_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Region patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def region_create_invalid_pair(
    region_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**region_create_mandatory_data}
    data[k] = v
    return data


@fixture
def region_create_duplicate_block_storage_services(
    region_create_mandatory_data: Dict[str, Any],
    block_storage_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = BlockStorageServiceCreateExtended(
        **block_storage_service_create_mandatory_data
    )
    return {
        **region_create_mandatory_data,
        "block_storage_services": [service, service],
    }


@fixture
def region_create_duplicate_compute_services(
    region_create_mandatory_data: Dict[str, Any],
    compute_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = ComputeServiceCreateExtended(**compute_service_create_mandatory_data)
    return {**region_create_mandatory_data, "compute_services": [service, service]}


@fixture
def region_create_duplicate_identity_services(
    region_create_mandatory_data: Dict[str, Any],
    identity_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = IdentityServiceCreate(**identity_service_create_mandatory_data)
    return {**region_create_mandatory_data, "identity_services": [service, service]}


@fixture
def region_create_duplicate_network_services(
    region_create_mandatory_data: Dict[str, Any],
    network_service_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Invalid case: the project list has duplicate values."""
    service = NetworkServiceCreateExtended(**network_service_create_mandatory_data)
    return {**region_create_mandatory_data, "network_services": [service, service]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("region_create_invalid_pair"),
        fixture_ref("region_create_duplicate_block_storage_services"),
        fixture_ref("region_create_duplicate_compute_services"),
        fixture_ref("region_create_duplicate_identity_services"),
        fixture_ref("region_create_duplicate_network_services"),
    },
)
def region_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a Region create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def region_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Region patch schema."""
    return {k: v}


@fixture
def region_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a Region patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("region_patch_valid_data_single_attr"),
        fixture_ref("region_patch_valid_data_for_tags"),
    },
)
def region_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Region patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def region_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Region patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
def db_region_simple(
    region_create_mandatory_data: Dict[str, Any],
    db_provider_with_projects: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_mandatory_data)
    return region_mng.create(obj_in=item, provider=db_provider_with_projects)


@fixture
def db_region_with_location(
    region_create_data_with_location: Dict[str, Any],
    db_provider_with_projects: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_location)
    return region_mng.create(obj_in=item, provider=db_provider_with_projects)


@fixture
def db_region_with_block_storage_services(
    region_create_data_with_block_storage_services: Dict[str, Any],
    db_provider_with_projects: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_block_storage_services)
    return region_mng.create(obj_in=item, provider=db_provider_with_projects)


@fixture
def db_region_with_compute_services(
    region_create_data_with_compute_services: Dict[str, Any],
    db_provider_with_projects: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_compute_services)
    return region_mng.create(obj_in=item, provider=db_provider_with_projects)


@fixture
def db_region_with_identity_services(
    region_create_data_with_identity_services: Dict[str, Any],
    db_provider_with_projects: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_identity_services)
    return region_mng.create(obj_in=item, provider=db_provider_with_projects)


@fixture
def db_region_with_network_services(
    region_create_data_with_network_services: Dict[str, Any],
    db_provider_with_projects: Provider,
) -> Region:
    """Fixture with standard DB Region."""
    item = RegionCreateExtended(**region_create_data_with_network_services)
    return region_mng.create(obj_in=item, provider=db_provider_with_projects)


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_region_simple"),
        fixture_ref("db_region_with_location"),
        fixture_ref("db_region_with_block_storage_services"),
        fixture_ref("db_region_with_compute_services"),
        fixture_ref("db_region_with_identity_services"),
        fixture_ref("db_region_with_network_services"),
    },
)
def db_region(db_item: Region) -> Region:
    """Generic DB Region instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def region_valid_create_schema_tuple(
    region_create_validator, region_create_valid_data
) -> Tuple[
    Type[RegionCreateExtended],
    CreateSchemaValidation[RegionBase, RegionBasePublic, RegionCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return RegionCreateExtended, region_create_validator, region_create_valid_data


@fixture
def region_invalid_create_schema_tuple(
    region_create_invalid_data,
) -> Tuple[Type[RegionCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return RegionCreateExtended, region_create_invalid_data


@fixture
def region_valid_patch_schema_tuple(
    region_patch_validator, region_patch_valid_data
) -> Tuple[
    Type[RegionUpdate],
    BaseSchemaValidation[RegionBase, RegionBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return RegionUpdate, region_patch_validator, region_patch_valid_data


@fixture
def region_invalid_patch_schema_tuple(
    region_patch_invalid_data,
) -> Tuple[Type[RegionUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return RegionUpdate, region_patch_invalid_data


@fixture
def region_valid_read_schema_tuple(
    region_read_class, region_read_validator, db_region
) -> Tuple[
    Union[RegionRead, RegionReadPublic, RegionReadExtended, RegionReadExtendedPublic],
    ReadSchemaValidation[
        RegionBase,
        RegionBasePublic,
        RegionRead,
        RegionReadPublic,
        RegionReadExtended,
        RegionReadExtendedPublic,
        Region,
    ],
    Region,
]:
    """Fixture with the read class, validator and the db item to read."""
    return region_read_class, region_read_validator, db_region
