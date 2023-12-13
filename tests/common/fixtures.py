"""Cases with tuples for SchemaCases."""
from pytest_cases import fixture, fixture_ref, parametrize

from app.flavor.schemas import FlavorUpdate
from app.provider.schemas_extended import FlavorCreateExtended


@fixture
@parametrize(
    "cls, validator, data",
    {
        (
            FlavorCreateExtended,
            fixture_ref("flavor_create_validator"),
            fixture_ref("flavor_create_valid_data"),
        ),
    },
)
def valid_create_schema_tuples(cls, validator, data):
    """Parametrized tuple with the items to use in 'case_valid_create_schema'."""
    return cls, validator, data


@fixture
@parametrize(
    "cls, data",
    {
        (FlavorCreateExtended, fixture_ref("flavor_create_invalid_data")),
    },
)
def invalid_create_schema_tuples(cls, data):
    """Parametrized tuple with the items to use in 'case_invalid_create_schema'."""
    return cls, data


@fixture
@parametrize(
    "cls, validator, data",
    {
        (
            FlavorUpdate,
            fixture_ref("flavor_patch_validator"),
            fixture_ref("flavor_patch_valid_data"),
        ),
    },
)
def valid_patch_schema_tuples(cls, validator, data):
    """Parametrized tuple with the items to use in 'case_valid_patch_schema'."""
    return cls, validator, data


@fixture
@parametrize(
    "cls, data",
    {
        (FlavorUpdate, fixture_ref("flavor_patch_invalid_data")),
    },
)
def invalid_patch_schema_tuples(cls, data):
    """Parametrized tuple with the items to use in 'case_invalid_patch_schema'."""
    return cls, data


@fixture
@parametrize(
    "cls, validator, db_item",
    {
        (
            fixture_ref("flavor_read_class"),
            fixture_ref("flavor_read_validator"),
            fixture_ref("db_flavor"),
        ),
    },
)
def valid_read_schema_tuples(cls, validator, db_item):
    """Parametrized tuple with the items to use in 'case_invalid_patch_schema'."""
    return cls, validator, db_item
