"""SLA specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.models import Provider
from app.provider.schemas_extended import SLACreateExtended
from app.region.models import Region
from app.service.models import ComputeService
from app.sla.crud import sla_mng
from app.sla.models import SLA
from app.sla.schemas import (
    SLABase,
    SLABasePublic,
    SLARead,
    SLAReadPublic,
    SLAUpdate,
)
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.utils import random_date, random_lower_string

invalid_create_key_values = {
    ("description", None),
    ("doc_uuid", None),
    ("start_date", None),
    ("end_date", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("doc_uuid", uuid4()),
    ("start_date", random_date()),
    ("end_date", random_date()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def sla_create_validator() -> (
    CreateSchemaValidation[SLABase, SLABasePublic, SLACreateExtended]
):
    """Instance to validate sla create schemas."""
    return CreateSchemaValidation[SLABase, SLABasePublic, SLACreateExtended](
        base=SLABase, base_public=SLABasePublic, create=SLACreateExtended
    )


@fixture(scope="package")
def sla_read_validator() -> (
    ReadSchemaValidation[
        SLABase,
        SLABasePublic,
        SLARead,
        SLAReadPublic,
        SLAReadExtended,
        SLAReadExtendedPublic,
        SLA,
    ]
):
    """Instance to validate sla read schemas."""
    return ReadSchemaValidation[
        SLABase,
        SLABasePublic,
        SLARead,
        SLAReadPublic,
        SLAReadExtended,
        SLAReadExtendedPublic,
        SLA,
    ](
        base=SLABase,
        base_public=SLABasePublic,
        read=SLARead,
        read_extended=SLAReadExtended,
    )


@fixture(scope="package")
def sla_patch_validator() -> BaseSchemaValidation[SLABase, SLABasePublic]:
    """Instance to validate sla patch schemas."""
    return BaseSchemaValidation[SLABase, SLABasePublic](
        base=SLABase, base_public=SLABasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {SLARead, SLAReadExtended, SLAReadPublic, SLAReadExtendedPublic},
)
def sla_read_class(cls) -> Any:
    """SLA Read schema."""
    return cls


# DICT FIXTURES


@fixture
def sla_create_mandatory_data() -> Dict[str, Any]:
    """Dict with SLA mandatory attributes."""
    d1 = random_date()
    d2 = random_date()
    if d1 < d2:
        start_date = d1
        end_date = d2
    else:
        start_date = d2
        end_date = d1
    return {"doc_uuid": uuid4(), "start_date": start_date, "end_date": end_date}


@fixture
def sla_create_all_data(sla_create_mandatory_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with all SLA attributes."""
    return {**sla_create_mandatory_data, "description": random_lower_string()}


@fixture
def sla_create_data_with_rel(sla_create_all_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**sla_create_all_data, "project": uuid4()}


@fixture
@parametrize("data", {fixture_ref("sla_create_data_with_rel")})
def sla_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a SLA patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def sla_create_invalid_pair(
    sla_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**sla_create_mandatory_data}
    data[k] = v
    return data


@fixture
@parametrize(
    "data",
    {
        fixture_ref("sla_create_mandatory_data"),
        fixture_ref("sla_create_invalid_pair"),
    },
)
def sla_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a SLA create schema."""
    return data


@fixture
@parametrize("k, v", patch_key_values)
def sla_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a SLA patch schema."""
    return {k: v}


@fixture
def sla_patch_valid_data_for_tags() -> Dict[str, Any]:
    """Valid set of attributes for a SLA patch schema. Tags details."""
    return {"tags": [random_lower_string()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("sla_patch_valid_data_single_attr"),
        fixture_ref("sla_patch_valid_data_for_tags"),
    },
)
def sla_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a SLA patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def sla_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a SLA patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_sla_simple(
    owned_projects: int,
    sla_create_mandatory_data: Dict[str, Any],
    db_compute_serv2: ComputeService,
) -> SLA:
    """Fixture with standard DB SLA.

    The sla can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = SLACreateExtended(
        **sla_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return sla_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_sla(
    sla_create_mandatory_data: Dict[str, Any],
    db_sla_simple: SLA,
    db_compute_serv3: ComputeService,
) -> SLA:
    """SLA shared within multiple services."""
    d = {}
    for k in sla_create_mandatory_data.keys():
        d[k] = db_sla_simple.__getattribute__(k)
    projects = [i.uuid for i in db_sla_simple.projects]
    item = SLACreateExtended(**d, is_public=len(projects) == 0, projects=projects)
    return sla_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize("db_item", {fixture_ref("db_sla_simple"), fixture_ref("db_shared_sla")})
def db_sla(db_item: SLA) -> SLA:
    """Generic DB SLA instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def sla_valid_create_schema_tuple(
    sla_create_validator, sla_create_valid_data
) -> Tuple[
    Type[SLACreateExtended],
    CreateSchemaValidation[SLABase, SLABasePublic, SLACreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return SLACreateExtended, sla_create_validator, sla_create_valid_data


@fixture
def sla_invalid_create_schema_tuple(
    sla_create_invalid_data,
) -> Tuple[Type[SLACreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return SLACreateExtended, sla_create_invalid_data


@fixture
def sla_valid_patch_schema_tuple(
    sla_patch_validator, sla_patch_valid_data
) -> Tuple[
    Type[SLAUpdate],
    BaseSchemaValidation[SLABase, SLABasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return SLAUpdate, sla_patch_validator, sla_patch_valid_data


@fixture
def sla_invalid_patch_schema_tuple(
    sla_patch_invalid_data,
) -> Tuple[Type[SLAUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return SLAUpdate, sla_patch_invalid_data


@fixture
def sla_valid_read_schema_tuple(
    sla_read_class, sla_read_validator, db_sla
) -> Tuple[
    Union[SLARead, SLAReadPublic, SLAReadExtended, SLAReadExtendedPublic],
    ReadSchemaValidation[
        SLABase,
        SLABasePublic,
        SLARead,
        SLAReadPublic,
        SLAReadExtended,
        SLAReadExtendedPublic,
        SLA,
    ],
    SLA,
]:
    """Fixture with the read class, validator and the db item to read."""
    return sla_read_class, sla_read_validator, db_sla
