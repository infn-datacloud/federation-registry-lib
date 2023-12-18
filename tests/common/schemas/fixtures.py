"""Cases with tuples for SchemaCases."""
from pytest_cases import fixture, fixture_ref, parametrize


@fixture
@parametrize(
    "cls, validator, data",
    [
        fixture_ref("flavor_create_valid_schema_actors"),
        fixture_ref("identity_provider_create_valid_schema_actors"),
        fixture_ref("image_create_valid_schema_actors"),
        fixture_ref("location_create_valid_schema_actors"),
        fixture_ref("network_create_valid_schema_actors"),
        fixture_ref("project_create_valid_schema_actors"),
        fixture_ref("provider_create_valid_schema_actors"),
        fixture_ref("block_storage_quota_create_valid_schema_actors"),
        fixture_ref("compute_quota_create_valid_schema_actors"),
        fixture_ref("network_quota_create_valid_schema_actors"),
        fixture_ref("region_create_valid_schema_actors"),
        fixture_ref("block_storage_service_create_valid_schema_actors"),
        fixture_ref("compute_service_create_valid_schema_actors"),
        fixture_ref("identity_service_create_valid_schema_actors"),
        fixture_ref("network_service_create_valid_schema_actors"),
        fixture_ref("sla_create_valid_schema_actors"),
        fixture_ref("user_group_create_valid_schema_actors"),
    ],
)
def valid_create_schema_tuples(cls, validator, data):
    """Parametrized tuple with the items to use in 'case_valid_create_schema'."""
    return cls, validator, data


@fixture
@parametrize(
    "cls, data",
    [
        fixture_ref("flavor_create_invalid_schema_actors"),
        fixture_ref("identity_provider_create_invalid_schema_actors"),
        fixture_ref("image_create_invalid_schema_actors"),
        fixture_ref("location_create_invalid_schema_actors"),
        fixture_ref("network_create_invalid_schema_actors"),
        fixture_ref("project_create_invalid_schema_actors"),
        fixture_ref("provider_create_invalid_schema_actors"),
        fixture_ref("block_storage_quota_create_invalid_schema_actors"),
        fixture_ref("compute_quota_create_invalid_schema_actors"),
        fixture_ref("network_quota_create_invalid_schema_actors"),
        fixture_ref("region_create_invalid_schema_actors"),
        fixture_ref("block_storage_service_create_invalid_schema_actors"),
        fixture_ref("compute_service_create_invalid_schema_actors"),
        fixture_ref("identity_service_create_invalid_schema_actors"),
        fixture_ref("network_service_create_invalid_schema_actors"),
        fixture_ref("sla_create_invalid_schema_actors"),
        fixture_ref("user_group_create_invalid_schema_actors"),
    ],
)
def invalid_create_schema_tuples(cls, data):
    """Parametrized tuple with the items to use in 'case_invalid_create_schema'."""
    return cls, data


@fixture
@parametrize(
    "cls, validator, data",
    [
        fixture_ref("flavor_patch_valid_schema_actors"),
        fixture_ref("identity_provider_patch_valid_schema_actors"),
        fixture_ref("image_patch_valid_schema_actors"),
        fixture_ref("location_patch_valid_schema_actors"),
        fixture_ref("network_patch_valid_schema_actors"),
        fixture_ref("project_patch_valid_schema_actors"),
        fixture_ref("provider_patch_valid_schema_actors"),
        fixture_ref("block_storage_quota_patch_valid_schema_actors"),
        fixture_ref("compute_quota_patch_valid_schema_actors"),
        fixture_ref("network_quota_patch_valid_schema_actors"),
        fixture_ref("region_patch_valid_schema_actors"),
        fixture_ref("block_storage_service_patch_valid_schema_actors"),
        fixture_ref("compute_service_patch_valid_schema_actors"),
        fixture_ref("identity_service_patch_valid_schema_actors"),
        fixture_ref("network_service_patch_valid_schema_actors"),
        fixture_ref("sla_patch_valid_schema_actors"),
        fixture_ref("user_group_patch_valid_schema_actors"),
    ],
)
def valid_patch_schema_tuples(cls, validator, data):
    """Parametrized tuple with the items to use in 'case_valid_patch_schema'."""
    return cls, validator, data


@fixture
@parametrize(
    "cls, data",
    [
        fixture_ref("flavor_patch_invalid_schema_actors"),
        fixture_ref("identity_provider_patch_invalid_schema_actors"),
        fixture_ref("image_patch_invalid_schema_actors"),
        fixture_ref("location_patch_invalid_schema_actors"),
        fixture_ref("network_patch_invalid_schema_actors"),
        fixture_ref("project_patch_invalid_schema_actors"),
        fixture_ref("provider_patch_invalid_schema_actors"),
        fixture_ref("block_storage_quota_patch_invalid_schema_actors"),
        fixture_ref("compute_quota_patch_invalid_schema_actors"),
        fixture_ref("network_quota_patch_invalid_schema_actors"),
        fixture_ref("region_patch_invalid_schema_actors"),
        fixture_ref("block_storage_service_patch_invalid_schema_actors"),
        fixture_ref("compute_service_patch_invalid_schema_actors"),
        fixture_ref("identity_service_patch_invalid_schema_actors"),
        fixture_ref("network_service_patch_invalid_schema_actors"),
        fixture_ref("sla_patch_invalid_schema_actors"),
        fixture_ref("user_group_patch_invalid_schema_actors"),
    ],
)
def invalid_patch_schema_tuples(cls, data):
    """Parametrized tuple with the items to use in 'case_invalid_patch_schema'."""
    return cls, data


@fixture
@parametrize(
    "cls, validator, db_item",
    [
        fixture_ref("flavor_valid_read_schema_tuple"),
        fixture_ref("identity_provider_valid_read_schema_tuple"),
        fixture_ref("image_valid_read_schema_tuple"),
        fixture_ref("location_valid_read_schema_tuple"),
        fixture_ref("network_valid_read_schema_tuple"),
        fixture_ref("project_valid_read_schema_tuple"),
        fixture_ref("provider_valid_read_schema_tuple"),
        fixture_ref("block_storage_quota_valid_read_schema_tuple"),
        fixture_ref("compute_quota_valid_read_schema_tuple"),
        fixture_ref("network_quota_valid_read_schema_tuple"),
        fixture_ref("region_valid_read_schema_tuple"),
        fixture_ref("block_storage_service_valid_read_schema_tuple"),
        fixture_ref("compute_service_valid_read_schema_tuple"),
        fixture_ref("identity_service_valid_read_schema_tuple"),
        fixture_ref("network_service_valid_read_schema_tuple"),
        fixture_ref("sla_valid_read_schema_tuple"),
        fixture_ref("user_group_valid_read_schema_tuple"),
    ],
)
def valid_read_schema_tuples(cls, validator, db_item):
    """Parametrized tuple with the items to use in 'case_valid_read_schema'."""
    return cls, validator, db_item
