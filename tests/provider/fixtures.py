"""Provider specific fixtures."""
from typing import Any, Dict, Tuple, Type, Union

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
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from tests.common.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)
from tests.utils.provider import random_status, random_type
from tests.utils.utils import random_bool, random_email, random_lower_string

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
def provider_mandatory_data() -> Dict[str, Any]:
    """Dict with Provider mandatory attributes."""
    return {"name": random_lower_string(), "type": random_type()}


@fixture
def provider_all_data(provider_mandatory_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with all Provider attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **provider_mandatory_data,
        "status": random_status(),
        "is_public": random_bool(),
        "support_emails": [random_email()],
    }


@fixture
@parametrize("data", {fixture_ref("provider_mandatory_data")})
def provider_create_valid_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Valid set of attributes for a Provider patch schema."""
    return data


@fixture
@parametrize("k, v", invalid_create_key_values)
def provider_create_invalid_pair(
    provider_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    data = {**provider_mandatory_data}
    data[k] = v
    return data


# TODO Add fixtures for duplicated values or complex relations raising ValidationError
# (see at the validator function of ProviderCreateExtended)


@fixture
@parametrize("data", {fixture_ref("provider_create_invalid_pair")})
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
def db_provider_simple(provider_mandatory_data: Dict[str, Any]) -> Provider:
    """Fixture with standard DB Provider."""
    item = ProviderCreateExtended(**provider_mandatory_data)
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
