"""IdentityProvider specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union
from uuid import uuid4

from pytest_cases import fixture, fixture_ref, parametrize

from app.identity_provider.crud import identity_provider_mng
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderBasePublic,
    IdentityProviderRead,
    IdentityProviderReadPublic,
    IdentityProviderUpdate,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
)
from app.provider.models import Provider
from app.provider.schemas_extended import (
    AuthMethodCreate,
    IdentityProviderCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from app.region.models import Region
from app.service.models import ComputeService
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.utils import random_date, random_lower_string, random_url

invalid_create_key_values = {
    ("description", None),
    ("endpoint", None),
    ("group_claim", None),
}
patch_key_values = {
    ("description", random_lower_string()),
    ("endpoint", random_url()),
    ("group_claim", random_lower_string()),
}
invalid_patch_key_values = {  # None is not accepted because there is a default
    ("description", None)
}
relationships_num = {0, 1, 2}


# CLASSES FIXTURES


@fixture(scope="package")
def identity_provider_create_validator() -> (
    CreateSchemaValidation[
        IdentityProviderBase, IdentityProviderBasePublic, IdentityProviderCreateExtended
    ]
):
    """Instance to validate identity_provider create schemas."""
    return CreateSchemaValidation[
        IdentityProviderBase, IdentityProviderBasePublic, IdentityProviderCreateExtended
    ](
        base=IdentityProviderBase,
        base_public=IdentityProviderBasePublic,
        create=IdentityProviderCreateExtended,
    )


@fixture(scope="package")
def identity_provider_read_validator() -> (
    ReadSchemaValidation[
        IdentityProviderBase,
        IdentityProviderBasePublic,
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
        IdentityProvider,
    ]
):
    """Instance to validate identity_provider read schemas."""
    return ReadSchemaValidation[
        IdentityProviderBase,
        IdentityProviderBasePublic,
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
        IdentityProvider,
    ](
        base=IdentityProviderBase,
        base_public=IdentityProviderBasePublic,
        read=IdentityProviderRead,
        read_extended=IdentityProviderReadExtended,
    )


@fixture(scope="package")
def identity_provider_patch_validator() -> (
    BaseSchemaValidation[IdentityProviderBase, IdentityProviderBasePublic]
):
    """Instance to validate identity_provider patch schemas."""
    return BaseSchemaValidation[IdentityProviderBase, IdentityProviderBasePublic](
        base=IdentityProviderBase, base_public=IdentityProviderBasePublic
    )


@fixture(scope="package")
@parametrize(
    "cls",
    {
        IdentityProviderRead,
        IdentityProviderReadExtended,
        IdentityProviderReadPublic,
        IdentityProviderReadExtendedPublic,
    },
)
def identity_provider_read_class(cls) -> Any:
    """IdentityProvider Read schema."""
    return cls


# DICT FIXTURES CREATE


@fixture
def identity_provider_create_mandatory_data() -> Dict[str, Any]:
    """Dict with IdentityProvider mandatory attributes."""
    return {"endpoint": random_url(), "group_claim": random_lower_string()}


@fixture
def identity_provider_create_all_data(
    identity_provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Dict with all IdentityProvider attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **identity_provider_create_mandatory_data,
        "description": random_lower_string(),
    }


@fixture
def identity_provider_create_data_with_rel() -> Dict[str, Any]:
    """Dict with IdentityProvider mandatory attributes."""
    d1 = random_date()
    d2 = random_date()
    if d1 < d2:
        start_date = d1
        end_date = d2
    else:
        start_date = d2
        end_date = d1
    return {
        "endpoint": random_url(),
        "group_claim": random_lower_string(),
        "relationship": AuthMethodCreate(
            idp_name=random_lower_string(), protocol=random_lower_string()
        ),
        "user_groups": [
            UserGroupCreateExtended(
                name=random_lower_string(),
                sla=SLACreateExtended(
                    doc_uuid=uuid4(),
                    start_date=start_date,
                    end_date=end_date,
                    project=uuid4(),
                ),
            )
        ],
    }


@fixture
@parametrize("data", {fixture_ref("identity_provider_create_data_with_rel")})
def identity_provider_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a IdentityProvider patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def identity_provider_create_invalid_pair(
    identity_provider_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**identity_provider_create_mandatory_data}
    data[k] = v
    return data


@fixture
def identity_provider_create_invalid_user_group_list_size(
    identity_provider_create_mandatory_data: Dict[str, Any],
) -> Dict[str, Any]:
    """User group list can't be empty."""
    return {**identity_provider_create_mandatory_data, "user_groups": []}


@fixture
def identity_provider_create_duplicate_user_groups(
    identity_provider_create_mandatory_data: Dict[str, Any],
    user_group_create_mandatory_data: Dict[str, Any],
):
    """Invalid case: the user group list has duplicate values."""
    d1 = random_date()
    d2 = random_date()
    if d1 < d2:
        start_date = d1
        end_date = d2
    else:
        start_date = d2
        end_date = d1
    user_group = UserGroupCreateExtended(
        **user_group_create_mandatory_data,
        sla=SLACreateExtended(
            doc_uuid=uuid4(),
            start_date=start_date,
            end_date=end_date,
            project=uuid4(),
        ),
    )
    return {
        **identity_provider_create_mandatory_data,
        "user_groups": [user_group, user_group],
    }


@fixture
@parametrize(
    "data",
    {
        fixture_ref("identity_provider_create_mandatory_data"),  # Missing user_groups
        fixture_ref("identity_provider_create_invalid_pair"),
        fixture_ref("identity_provider_create_invalid_user_group_list_size"),
        fixture_ref("identity_provider_create_duplicate_user_groups"),
    },
)
def identity_provider_create_invalid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Invalid set of attributes for a IdentityProvider create schema."""
    return data


# DICT FIXTURES PATCH


@fixture
@parametrize("k, v", patch_key_values)
def identity_provider_patch_valid_data_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a IdentityProvider patch schema."""
    return {k: v}


@fixture
@parametrize("data", {fixture_ref("identity_provider_patch_valid_data_single_attr")})
def identity_provider_patch_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a IdentityProvider patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_patch_key_values)
def identity_provider_patch_invalid_data(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a IdentityProvider patch schema."""
    return {k: v}


# DB INSTANCES FIXTURES


@fixture
@parametrize("owned_projects", relationships_num)
def db_identity_provider_simple(
    owned_projects: int,
    identity_provider_create_mandatory_data: Dict[str, Any],
    db_compute_serv2: ComputeService,
) -> IdentityProvider:
    """Fixture with standard DB IdentityProvider.

    The identity_provider can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = IdentityProviderCreateExtended(
        **identity_provider_create_mandatory_data,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return identity_provider_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_identity_provider(
    identity_provider_create_mandatory_data: Dict[str, Any],
    db_identity_provider_simple: IdentityProvider,
    db_compute_serv3: ComputeService,
) -> IdentityProvider:
    """IdentityProvider shared within multiple services."""
    d = {}
    for k in identity_provider_create_mandatory_data.keys():
        d[k] = db_identity_provider_simple.__getattribute__(k)
    projects = [i.uuid for i in db_identity_provider_simple.projects]
    item = IdentityProviderCreateExtended(
        **d, is_public=len(projects) == 0, projects=projects
    )
    return identity_provider_mng.create(obj_in=item, service=db_compute_serv3)


@fixture
@parametrize(
    "db_item",
    {
        fixture_ref("db_identity_provider_simple"),
        fixture_ref("db_shared_identity_provider"),
    },
)
def db_identity_provider(db_item: IdentityProvider) -> IdentityProvider:
    """Generic DB IdentityProvider instance."""
    return db_item


# TUPLE FOR CASES FIXTURES


@fixture
def identity_provider_valid_create_schema_tuple(
    identity_provider_create_validator, identity_provider_create_valid_data
) -> Tuple[
    Type[IdentityProviderCreateExtended],
    CreateSchemaValidation[
        IdentityProviderBase, IdentityProviderBasePublic, IdentityProviderCreateExtended
    ],
    Dict[str, Any],
]:
    """Fixture with the create class, validator and data to validate."""
    return (
        IdentityProviderCreateExtended,
        identity_provider_create_validator,
        identity_provider_create_valid_data,
    )


@fixture
def identity_provider_invalid_create_schema_tuple(
    identity_provider_create_invalid_data,
) -> Tuple[Type[IdentityProviderCreateExtended], Dict[str, Any]]:
    """Fixture with the create class and the invalid data to validate."""
    return IdentityProviderCreateExtended, identity_provider_create_invalid_data


@fixture
def identity_provider_valid_patch_schema_tuple(
    identity_provider_patch_validator, identity_provider_patch_valid_data
) -> Tuple[
    Type[IdentityProviderUpdate],
    BaseSchemaValidation[IdentityProviderBase, IdentityProviderBasePublic],
    Dict[str, Any],
]:
    """Fixture with the update class, validator and data to validate."""
    return (
        IdentityProviderUpdate,
        identity_provider_patch_validator,
        identity_provider_patch_valid_data,
    )


@fixture
def identity_provider_invalid_patch_schema_tuple(
    identity_provider_patch_invalid_data,
) -> Tuple[Type[IdentityProviderUpdate], Dict[str, Any]]:
    """Fixture with the update class and the invalid data to validate."""
    return IdentityProviderUpdate, identity_provider_patch_invalid_data


@fixture
def identity_provider_valid_read_schema_tuple(
    identity_provider_read_class, identity_provider_read_validator, db_identity_provider
) -> Tuple[
    Union[
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
    ],
    ReadSchemaValidation[
        IdentityProviderBase,
        IdentityProviderBasePublic,
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
        IdentityProvider,
    ],
    IdentityProvider,
]:
    """Fixture with the read class, validator and the db item to read."""
    return (
        identity_provider_read_class,
        identity_provider_read_validator,
        db_identity_provider,
    )
