"""Cases with tuples for SchemaCases."""
from pytest_cases import fixture, fixture_ref, parametrize


@fixture
@parametrize(
    "cls, validator, data",
    {
        fixture_ref("flavor_valid_create_schema_tuple"),
        fixture_ref("image_valid_create_schema_tuple"),
        fixture_ref("location_valid_create_schema_tuple"),
        fixture_ref("network_valid_create_schema_tuple"),
    },
)
def valid_create_schema_tuples(cls, validator, data):
    """Parametrized tuple with the items to use in 'case_valid_create_schema'."""
    return cls, validator, data


@fixture
@parametrize(
    "cls, data",
    {
        fixture_ref("flavor_invalid_create_schema_tuple"),
        fixture_ref("image_invalid_create_schema_tuple"),
        fixture_ref("location_invalid_create_schema_tuple"),
        fixture_ref("network_invalid_create_schema_tuple"),
    },
)
def invalid_create_schema_tuples(cls, data):
    """Parametrized tuple with the items to use in 'case_invalid_create_schema'."""
    return cls, data


@fixture
@parametrize(
    "cls, validator, data",
    {
        fixture_ref("flavor_valid_patch_schema_tuple"),
        fixture_ref("image_valid_patch_schema_tuple"),
        fixture_ref("location_valid_patch_schema_tuple"),
        fixture_ref("network_valid_patch_schema_tuple"),
    },
)
def valid_patch_schema_tuples(cls, validator, data):
    """Parametrized tuple with the items to use in 'case_valid_patch_schema'."""
    return cls, validator, data


@fixture
@parametrize(
    "cls, data",
    {
        fixture_ref("flavor_invalid_patch_schema_tuple"),
        fixture_ref("image_invalid_patch_schema_tuple"),
        fixture_ref("location_invalid_patch_schema_tuple"),
        fixture_ref("network_invalid_patch_schema_tuple"),
    },
)
def invalid_patch_schema_tuples(cls, data):
    """Parametrized tuple with the items to use in 'case_invalid_patch_schema'."""
    return cls, data


@fixture
@parametrize(
    "cls, validator, db_item",
    {
        fixture_ref("flavor_valid_read_schema_tuple"),
        fixture_ref("image_valid_read_schema_tuple"),
        fixture_ref("location_valid_read_schema_tuple"),
        fixture_ref("network_valid_read_schema_tuple"),
    },
)
def valid_read_schema_tuples(cls, validator, db_item):
    """Parametrized tuple with the items to use in 'case_invalid_patch_schema'."""
    return cls, validator, db_item
