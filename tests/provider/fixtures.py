"""Provider specific fixtures."""
from typing import Any, Dict, List, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.provider.crud import provider_mng
from app.provider.models import Provider
from app.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderRead,
    ProviderReadPublic,
    ProviderUpdate,
)
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
    ProjectCreate,
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
    RegionCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.provider import random_status, random_type
from tests.utils.utils import (
    random_bool,
    random_date,
    random_email,
    random_lower_string,
    random_url,
)

invalid_create_key_values = {
    ("description", None),
    ("name", None),
    ("type", None),
    ("type", random_lower_string()),
    ("status", None),
    ("status", random_lower_string()),
    ("is_public", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("name", random_lower_string()),
    ("type", random_type()),
    ("status", random_status()),
    ("is_public", random_bool()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None),
    ("type", random_lower_string()),
    ("status", None),
    ("status", random_lower_string()),
    ("is_public", None),
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def provider_create_validator() -> (
    CreateSchemaValidation[ProviderBase, ProviderBasePublic, ProviderCreateExtended]
):
    """Instance to validate provider create schemas."""
    return CreateSchemaValidation[
        ProviderBase, ProviderBasePublic, ProviderCreateExtended
    ](base=ProviderBase, base_public=ProviderBasePublic, create=ProviderCreateExtended)


@fixture(scope="package")
def provider_read_validator() -> (
    ReadSchemaValidation[
        ProviderBase,
        ProviderBasePublic,
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
        Provider,
    ]
):
    """Instance to validate provider read schemas."""
    return ReadSchemaValidation[
        ProviderBase,
        ProviderBasePublic,
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
        Provider,
    ](
        base=ProviderBase,
        base_public=ProviderBasePublic,
        read=ProviderRead,
        read_extended=ProviderReadExtended,
    )


@fixture(scope="package")
def provider_patch_validator() -> (
    BaseSchemaValidation[ProviderBase, ProviderBasePublic]
):
    """Instance to validate provider patch schemas."""
    return BaseSchemaValidation[ProviderBase, ProviderBasePublic](
        base=ProviderBase, base_public=ProviderBasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        ProviderRead,
        ProviderReadExtended,
        ProviderReadPublic,
        ProviderReadExtendedPublic,
    },
)
def provider_read_class(cls) -> Any:
    """Provider Read schema."""
    return cls


# DICT FIXTURES


@fixture
def provider_create_mandatory_data() -> Dict[str, Any]:
    """Dict with Provider mandatory attributes."""
    return {"name": random_lower_string(), "type": random_type()}


@fixture
def provider_create_all_data(
    provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes."""
    return {
        **provider_create_mandatory_data,
        "description": random_lower_string(),
        "status": random_status(),
        "is_public": random_bool(),
        "support_emails": [random_email()],
    }


@fixture
@parametrize(owned_regions=relationships_num)
def provider_create_data_with_regions(
    owned_regions: int,
    provider_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    regions = []
    for _ in range(owned_regions):
        regions.append(RegionCreateExtended(name=random_lower_string()))
    return {**provider_create_all_data, "regions": regions}


@fixture
@parametrize(
    owned_projects=relationships_num,
)
def provider_create_data_with_projects(
    owned_projects: int,
    provider_create_all_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects = []
    for _ in range(owned_projects):
        projects.append(ProjectCreate(name=random_lower_string(), uuid=uuid4()))
    return {**provider_create_all_data, "projects": projects}


@fixture
def provider_create_data_with_idps(
    provider_create_data_with_projects: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects: List[ProjectCreate] = provider_create_data_with_projects.get("projects")
    identity_providers = []
    for i in range(len(projects)):
        d1 = random_date()
        d2 = random_date()
        if d1 < d2:
            start_date = d1
            end_date = d2
        else:
            start_date = d2
            end_date = d1
        identity_providers.append(
            IdentityProviderCreateExtended(
                endpoint=random_url(),
                group_claim=random_lower_string(),
                relationship=AuthMethodCreate(
                    idp_name=random_lower_string(), protocol=random_lower_string()
                ),
                user_groups=[
                    UserGroupCreateExtended(
                        name=random_lower_string(),
                        sla=SLACreateExtended(
                            doc_uuid=uuid4(),
                            start_date=start_date,
                            end_date=end_date,
                            project=projects[i].uuid,
                        ),
                    )
                ],
            )
        )
    return {
        **provider_create_data_with_projects,
        "identity_providers": identity_providers,
    }


@fixture
@parametrize(
    "data",
    {
        fixture_ref("provider_create_mandatory_data"),
        fixture_ref("provider_create_data_with_regions"),
        fixture_ref("provider_create_data_with_idps"),  # Include case with projects
    },
)
def provider_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Provider patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def provider_create_invalid_pair(
    provider_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**provider_create_mandatory_data}
    data[k] = v
    return data


@fixture
def provider_create_duplicate_regions(
    provider_create_all_data: Dict[str, Any],
    region_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    region = RegionCreateExtended(**region_create_mandatory_data)
    return {**provider_create_all_data, "regions": [region, region]}


@fixture
def provider_create_duplicate_projects(
    provider_create_all_data: Dict[str, Any],
    project_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    project = ProjectCreate(**project_create_mandatory_data)
    return {**provider_create_all_data, "projects": [project, project]}


@fixture
def provider_create_duplicate_idps(
    provider_create_all_data: Dict[str, Any],
    identity_provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all Provider attributes and regions."""
    projects = [
        ProjectCreate(name=random_lower_string(), uuid=uuid4()),
        ProjectCreate(name=random_lower_string(), uuid=uuid4()),
    ]
    identity_providers = []
    for i in range(len(projects)):
        d1 = random_date()
        d2 = random_date()
        if d1 < d2:
            start_date = d1
            end_date = d2
        else:
            start_date = d2
            end_date = d1
        identity_providers.append(
            IdentityProviderCreateExtended(
                **identity_provider_create_mandatory_data,
                relationship=AuthMethodCreate(
                    idp_name=random_lower_string(), protocol=random_lower_string()
                ),
                user_groups=[
                    UserGroupCreateExtended(
                        name=random_lower_string(),
                        sla=SLACreateExtended(
                            doc_uuid=uuid4(),
                            start_date=start_date,
                            end_date=end_date,
                            project=projects[i].uuid,
                        ),
                    )
                ],
            )
        )
    return {
        **provider_create_all_data,
        "projects": projects,
        "identity_providers": identity_providers,
    }


# TODO Add fixtures for invalid create cases:
# (see at the validator function of ProviderCreateExtended)
# - check_idp_projs_exits
# - check_block_storage_serv_projs_exist
# - check_compute_serv_projs_exist
# - check_network_serv_projs_exist


@fixture
@parametrize(
    "data",
    {
        fixture_ref("provider_create_invalid_pair"),
        fixture_ref("provider_create_duplicate_regions"),
        fixture_ref("provider_create_duplicate_projects"),
        fixture_ref("provider_create_duplicate_idps"),
    },
)
def provider_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a Provider create schema."""
    return data


@fixture
@parametrize("k, v", patch_key_values)
def provider_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a Provider patch schema."""
    return {k: v}


@fixture
def provider_patch_valid_data_for_support_emails() -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema. Tags details."""
    return {"support_emails": [random_email()]}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("provider_patch_valid_data_single_attr"),
        fixture_ref("provider_patch_valid_data_for_support_emails"),
    },
)
def provider_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Provider patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def provider_patch_invalid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a Provider patch schema."""
    return {k: v}


@fixture
@parametrize("support_emails", {None, random_lower_string()})
def provider_patch_invalid_data_for_support_emails(support_emails) -> Dict[str, Any]:
    """Valid set of attributes for a Image patch schema. Tags details."""
    support_emails = [support_emails] if support_emails else support_emails
    return {"support_emails": support_emails}


@fixture
@parametrize(
    "data",
    {
        fixture_ref("provider_patch_invalid_data_single_attr"),
        fixture_ref("provider_patch_invalid_data_for_support_emails"),
    },
)
def provider_patch_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Provider patch schema."""
    return data


# DB INSTANCES FIXTURES


@fixture
def db_provider_simple(provider_create_mandatory_data: Dict[str, Any]) -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**provider_create_mandatory_data)
    return provider_mng.create(obj_in=item)


@fixture
@parametrize("db_item", {fixture_ref("db_provider_simple")})
def db_provider(db_item: Provider) -> Provider:
    """Generic DB Provider instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def provider_valid_create_schema_tuple(
    provider_create_validator, provider_create_valid_data
) -> Tuple[
    Type[ProviderCreateExtended],
    CreateSchemaValidation[ProviderBase, ProviderBasePublic, ProviderCreateExtended],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return ProviderCreateExtended, provider_create_validator, provider_create_valid_data


@fixture
def provider_invalid_create_schema_tuple(
    provider_create_invalid_data,
) -> Tuple[Type[ProviderCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return ProviderCreateExtended, provider_create_invalid_data


@fixture
def provider_valid_patch_schema_tuple(
    provider_patch_validator, provider_patch_valid_data
) -> Tuple[
    Type[ProviderUpdate],
    BaseSchemaValidation[ProviderBase, ProviderBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return ProviderUpdate, provider_patch_validator, provider_patch_valid_data


@fixture
def provider_invalid_patch_schema_tuple(
    provider_patch_invalid_data,
) -> Tuple[Type[ProviderUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return ProviderUpdate, provider_patch_invalid_data


@fixture
def provider_valid_read_schema_tuple(
    provider_read_class, provider_read_validator, db_provider
) -> Tuple[
    Union[
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
    ],
    ReadSchemaValidation[
        ProviderBase,
        ProviderBasePublic,
        ProviderRead,
        ProviderReadPublic,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
        Provider,
    ],
    Provider,
]:
    """Fixture with the read class, validator and the db item to read."""
    return provider_read_class, provider_read_validator, db_provider
