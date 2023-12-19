"""Cases with actors for SchemaCases."""
from pytest_cases import fixture_union

valid_create_schema_actors = fixture_union(
    "valid_create_schema_actors",
    [
        "flavor_create_valid_schema_actors",
        "identity_provider_create_valid_schema_actors",
        "image_create_valid_schema_actors",
        "location_create_valid_schema_actors",
        "network_create_valid_schema_actors",
        "project_create_valid_schema_actors",
        "provider_create_valid_schema_actors",
        "block_storage_quota_create_valid_schema_actors",
        "compute_quota_create_valid_schema_actors",
        "network_quota_create_valid_schema_actors",
        "region_create_valid_schema_actors",
        "block_storage_service_create_valid_schema_actors",
        "compute_service_create_valid_schema_actors",
        "identity_service_create_valid_schema_actors",
        "network_service_create_valid_schema_actors",
        "sla_create_valid_schema_actors",
        "user_group_create_valid_schema_actors",
    ],
    idstyle="explicit",
)


invalid_create_schema_actors = fixture_union(
    "invalid_create_schema_actors",
    [
        "flavor_create_invalid_schema_actors",
        "identity_provider_create_invalid_schema_actors",
        "image_create_invalid_schema_actors",
        "location_create_invalid_schema_actors",
        "network_create_invalid_schema_actors",
        "project_create_invalid_schema_actors",
        "provider_create_invalid_schema_actors",
        "block_storage_quota_create_invalid_schema_actors",
        "compute_quota_create_invalid_schema_actors",
        "network_quota_create_invalid_schema_actors",
        "region_create_invalid_schema_actors",
        "block_storage_service_create_invalid_schema_actors",
        "compute_service_create_invalid_schema_actors",
        "identity_service_create_invalid_schema_actors",
        "network_service_create_invalid_schema_actors",
        "sla_create_invalid_schema_actors",
        "user_group_create_invalid_schema_actors",
    ],
    idstyle="explicit",
)


valid_patch_schema_actors = fixture_union(
    "valid_patch_schema_actors",
    [
        "flavor_patch_valid_schema_actors",
        "identity_provider_patch_valid_schema_actors",
        "image_patch_valid_schema_actors",
        "location_patch_valid_schema_actors",
        "network_patch_valid_schema_actors",
        "project_patch_valid_schema_actors",
        "provider_patch_valid_schema_actors",
        "block_storage_quota_patch_valid_schema_actors",
        "compute_quota_patch_valid_schema_actors",
        "network_quota_patch_valid_schema_actors",
        "region_patch_valid_schema_actors",
        "block_storage_service_patch_valid_schema_actors",
        "compute_service_patch_valid_schema_actors",
        "identity_service_patch_valid_schema_actors",
        "network_service_patch_valid_schema_actors",
        "sla_patch_valid_schema_actors",
        "user_group_patch_valid_schema_actors",
    ],
    idstyle="explicit",
)

invalid_patch_schema_actors = fixture_union(
    "invalid_patch_schema_actors",
    [
        "flavor_patch_invalid_schema_actors",
        "identity_provider_patch_invalid_schema_actors",
        "image_patch_invalid_schema_actors",
        "location_patch_invalid_schema_actors",
        "network_patch_invalid_schema_actors",
        "project_patch_invalid_schema_actors",
        "provider_patch_invalid_schema_actors",
        "block_storage_quota_patch_invalid_schema_actors",
        "compute_quota_patch_invalid_schema_actors",
        "network_quota_patch_invalid_schema_actors",
        "region_patch_invalid_schema_actors",
        "block_storage_service_patch_invalid_schema_actors",
        "compute_service_patch_invalid_schema_actors",
        "identity_service_patch_invalid_schema_actors",
        "network_service_patch_invalid_schema_actors",
        "sla_patch_invalid_schema_actors",
        "user_group_patch_invalid_schema_actors",
    ],
    idstyle="explicit",
)


valid_read_schema_actors = fixture_union(
    "valid_read_schema_actors",
    [
        "flavor_valid_read_schema_tuple",
        "identity_provider_valid_read_schema_tuple",
        "image_valid_read_schema_tuple",
        "location_valid_read_schema_tuple",
        "network_valid_read_schema_tuple",
        "project_valid_read_schema_tuple",
        "provider_valid_read_schema_tuple",
        "block_storage_quota_valid_read_schema_tuple",
        "compute_quota_valid_read_schema_tuple",
        "network_quota_valid_read_schema_tuple",
        "region_valid_read_schema_tuple",
        "block_storage_service_valid_read_schema_tuple",
        "compute_service_valid_read_schema_tuple",
        "identity_service_valid_read_schema_tuple",
        "network_service_valid_read_schema_tuple",
        "sla_valid_read_schema_tuple",
        "user_group_valid_read_schema_tuple",
    ],
    idstyle="explicit",
)
