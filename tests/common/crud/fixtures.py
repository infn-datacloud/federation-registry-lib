"""Cases with tuples for SchemaCases."""
from pytest_cases import fixture_union

create_item_actors = fixture_union(
    "create_item_actors",
    [
        # "flavor_valid_create_item_actors",
        # "identity_provider_valid_create_item_actors",
        # "image_valid_create_item_actors",
        # "location_valid_create_item_actors",
        # "network_valid_create_item_actors",
        # "project_valid_create_item_actors",
        "provider_create_item_actors",
        # "block_storage_quota_valid_create_item_actors",
        # "compute_quota_valid_create_item_actors",
        # "network_quota_valid_create_item_actors",
        # "region_valid_create_item_actors",
        # "block_storage_service_valid_create_item_actors",
        # "compute_service_valid_create_item_actors",
        # "identity_service_valid_create_item_actors",
        # "network_service_valid_create_item_actors",
        # "sla_valid_create_item_actors",
        # "user_group_valid_create_item_actors",
    ],
    idstyle="explicit",
)


valid_read_item_actors = fixture_union(
    "valid_read_item_actors",
    [
        # "flavor_read_item_actors",
        # "identity_provider_read_item_actors",
        # "image_read_item_actors",
        # "location_read_item_actors",
        # "network_read_item_actors",
        # "project_read_item_actors",
        "provider_read_item_actors",
        # "block_storage_quota_read_item_actors",
        # "compute_quota_read_item_actors",
        # "network_quota_read_item_actors",
        # "region_read_item_actors",
        # "block_storage_service_read_item_actors",
        # "compute_service_read_item_actors",
        # "identity_service_read_item_actors",
        # "network_service_read_item_actors",
        # "sla_read_item_actors",
        # "user_group_read_item_actors",
    ],
    idstyle="explicit",
)


valid_read_items_actors = fixture_union(
    "valid_read_items_actors",
    [
        # "flavor_read_items_actors",
        # "identity_provider_read_items_actors",
        # "image_read_items_actors",
        # "location_read_items_actors",
        # "network_read_items_actors",
        # "project_read_items_actors",
        "provider_read_items_actors",
        # "block_storage_quota_read_items_actors",
        # "compute_quota_read_items_actors",
        # "network_quota_read_items_actors",
        # "region_read_items_actors",
        # "block_storage_service_read_items_actors",
        # "compute_service_read_items_actors",
        # "identity_service_read_items_actors",
        # "network_service_read_items_actors",
        # "sla_read_items_actors",
        # "user_group_read_items_actors",
    ],
    idstyle="explicit",
)


delete_item_actors = fixture_union(
    "delete_item_actors",
    [
        # "flavor_delete_item_actors",
        # "identity_provider_delete_item_actors",
        # "image_delete_item_actors",
        # "location_delete_item_actors",
        # "network_delete_item_actors",
        # "project_delete_item_actors",
        "provider_delete_item_actors",
        # "block_storage_quota_delete_item_actors",
        # "compute_quota_delete_item_actors",
        # "network_quota_delete_item_actors",
        # "region_delete_item_actors",
        # "block_storage_service_delete_item_actors",
        # "compute_service_delete_item_actors",
        # "identity_service_delete_item_actors",
        # "network_service_delete_item_actors",
        # "sla_delete_item_actors",
        # "user_group_delete_item_actors",
    ],
    idstyle="explicit",
)


patch_item_actors = fixture_union(
    "patch_item_actors",
    [
        # "flavor_patch_item_actors",
        # "identity_provider_patch_item_actors",
        # "image_patch_item_actors",
        # "location_patch_item_actors",
        # "network_patch_item_actors",
        # "project_patch_item_actors",
        "provider_patch_item_actors",
        # "block_storage_quota_patch_item_actors",
        # "compute_quota_patch_item_actors",
        # "network_quota_patch_item_actors",
        # "region_patch_item_actors",
        # "block_storage_service_patch_item_actors",
        # "compute_service_patch_item_actors",
        # "identity_service_patch_item_actors",
        # "network_service_patch_item_actors",
        # "sla_patch_item_actors",
        # "user_group_patch_item_actors",
    ],
    idstyle="explicit",
)


patch_item_with_default_actors = fixture_union(
    "patch_item_with_default_actors",
    [
        # "flavor_patch_item_with_default_actors",
        # "identity_provider_patch_item_with_default_actors",
        # "image_patch_item_with_default_actors",
        # "location_patch_item_with_default_actors",
        # "network_patch_item_with_default_actors",
        # "project_patch_item_with_default_actors",
        "provider_patch_item_with_default_actors",
        # "block_storage_quota_patch_item_with_default_actors",
        # "compute_quota_patch_item_with_default_actors",
        # "network_quota_patch_item_with_default_actors",
        # "region_patch_item_with_default_actors",
        # "block_storage_service_patch_item_with_default_actors",
        # "compute_service_patch_item_with_default_actors",
        # "identity_service_patch_item_with_default_actors",
        # "network_service_patch_item_with_default_actors",
        # "sla_patch_item_with_default_actors",
        # "user_group_patch_item_with_default_actors",
    ],
    idstyle="explicit",
)


patch_item_required_with_none_actors = fixture_union(
    "patch_item_required_with_none_actors",
    [
        # "flavor_patch_item_required_with_none_actors",
        # "identity_provider_patch_item_required_with_none_actors",
        # "image_patch_item_required_with_none_actors",
        # "location_patch_item_required_with_none_actors",
        # "network_patch_item_required_with_none_actors",
        # "project_patch_item_required_with_none_actors",
        "provider_patch_item_required_with_none_actors",
        # "block_storage_quota_patch_item_required_with_none_actors",
        # "compute_quota_patch_item_required_with_none_actors",
        # "network_quota_patch_item_required_with_none_actors",
        # "region_patch_item_required_with_none_actors",
        # "block_storage_service_patch_item_required_with_none_actors",
        # "compute_service_patch_item_required_with_none_actors",
        # "identity_service_patch_item_required_with_none_actors",
        # "network_service_patch_item_required_with_none_actors",
        # "sla_patch_item_required_with_none_actors",
        # "user_group_patch_item_required_with_none_actors",
    ],
    idstyle="explicit",
)

patch_item_no_changes_actors = fixture_union(
    "patch_item_no_changes_actors",
    [
        # "flavor_patch_item_no_changes_actors",
        # "identity_provider_patch_item_no_changes_actors",
        # "image_patch_item_no_changes_actors",
        # "location_patch_item_no_changes_actors",
        # "network_patch_item_no_changes_actors",
        # "project_patch_item_no_changes_actors",
        "provider_patch_item_no_changes_actors",
        # "block_storage_quota_patch_item_no_changes_actors",
        # "compute_quota_patch_item_no_changes_actors",
        # "network_quota_patch_item_no_changes_actors",
        # "region_patch_item_no_changes_actors",
        # "block_storage_service_patch_item_no_changes_actors",
        # "compute_service_patch_item_no_changes_actors",
        # "identity_service_patch_item_no_changes_actors",
        # "network_service_patch_item_no_changes_actors",
        # "sla_patch_item_no_changes_actors",
        # "user_group_patch_item_no_changes_actors",
    ],
    idstyle="explicit",
)


not_existing_actors = fixture_union(
    "not_existing_actors",
    [
        # "flavor_not_existing_actors",
        # "identity_provider_not_existing_actors",
        # "image_not_existing_actors",
        # "location_not_existing_actors",
        # "network_not_existing_actors",
        # "project_not_existing_actors",
        "provider_not_existing_actors",
        # "block_storage_quota_not_existing_actors",
        # "compute_quota_not_existing_actors",
        # "network_quota_not_existing_actors",
        # "region_not_existing_actors",
        # "block_storage_service_not_existing_actors",
        # "compute_service_not_existing_actors",
        # "identity_service_not_existing_actors",
        # "network_service_not_existing_actors",
        # "sla_not_existing_actors",
        # "user_group_not_existing_actors",
    ],
    idstyle="explicit",
)


item_attr = fixture_union(
    "item_attr",
    [
        # "flavor_attr",
        # "identity_provider_attr",
        # "image_attr",
        # "location_attr",
        # "network_attr",
        # "project_attr",
        "provider_attr",
        # "block_storage_quota_attr",
        # "compute_quota_attr",
        # "network_quota_attr",
        # "region_attr",
        # "block_storage_service_attr",
        # "compute_service_attr",
        # "identity_service_attr",
        # "network_service_attr",
        # "sla_attr",
        # "user_group_attr",
    ],
    idstyle="explicit",
)
