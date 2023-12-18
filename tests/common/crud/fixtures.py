"""Cases with tuples for SchemaCases."""
from typing import Optional

from pytest_cases import fixture, fixture_ref, parametrize


@fixture
@parametrize(
    "manager, validator, schema, kwargs",
    [
        # fixture_ref("flavor_valid_create_item_tuple"),
        # fixture_ref("identity_provider_valid_create_item_tuple"),
        # fixture_ref("image_valid_create_item_tuple"),
        # fixture_ref("location_valid_create_item_tuple"),
        # fixture_ref("network_valid_create_item_tuple"),
        # fixture_ref("project_valid_create_item_tuple"),
        fixture_ref("provider_create_item_tuple"),
        # fixture_ref("block_storage_quota_valid_create_item_tuple"),
        # fixture_ref("compute_quota_valid_create_item_tuple"),
        # fixture_ref("network_quota_valid_create_item_tuple"),
        # fixture_ref("region_valid_create_item_tuple"),
        # fixture_ref("block_storage_service_valid_create_item_tuple"),
        # fixture_ref("compute_service_valid_create_item_tuple"),
        # fixture_ref("identity_service_valid_create_item_tuple"),
        # fixture_ref("network_service_valid_create_item_tuple"),
        # fixture_ref("sla_valid_create_item_tuple"),
        # fixture_ref("user_group_valid_create_item_tuple"),
    ],
)
def create_item_tuple(manager, validator, schema, kwargs):
    """Parametrized tuple with the items to use in 'case_valid_create_item'."""
    return manager, validator, schema, kwargs


# @fixture
# @parametrize(
#     "cls, validator, data",
#     [
#         fixture_ref("flavor_valid_patch_item_tuple"),
#         fixture_ref("identity_provider_valid_patch_item_tuple"),
#         fixture_ref("image_valid_patch_item_tuple"),
#         fixture_ref("location_valid_patch_item_tuple"),
#         fixture_ref("network_valid_patch_item_tuple"),
#         fixture_ref("project_valid_patch_item_tuple"),
#         fixture_ref("provider_valid_patch_item_tuple"),
#         fixture_ref("block_storage_quota_valid_patch_item_tuple"),
#         fixture_ref("compute_quota_valid_patch_item_tuple"),
#         fixture_ref("network_quota_valid_patch_item_tuple"),
#         fixture_ref("region_valid_patch_item_tuple"),
#         fixture_ref("block_storage_service_valid_patch_item_tuple"),
#         fixture_ref("compute_service_valid_patch_item_tuple"),
#         fixture_ref("identity_service_valid_patch_item_tuple"),
#         fixture_ref("network_service_valid_patch_item_tuple"),
#         fixture_ref("sla_valid_patch_item_tuple"),
#         fixture_ref("user_group_valid_patch_item_tuple"),
#     ],
# )
# def valid_patch_item_tuples(cls, validator, data):
#     """Parametrized tuple with the items to use in 'case_valid_patch_item'."""
#     return cls, validator, data


@fixture
@parametrize(
    "manager, validator, db_item",
    [
        # fixture_ref("flavor_valid_read_item_tuple"),
        # fixture_ref("identity_provider_valid_read_item_tuple"),
        # fixture_ref("image_valid_read_item_tuple"),
        # fixture_ref("location_valid_read_item_tuple"),
        # fixture_ref("network_valid_read_item_tuple"),
        # fixture_ref("project_valid_read_item_tuple"),
        fixture_ref("provider_valid_read_item_tuple"),
        # fixture_ref("block_storage_quota_valid_read_item_tuple"),
        # fixture_ref("compute_quota_valid_read_item_tuple"),
        # fixture_ref("network_quota_valid_read_item_tuple"),
        # fixture_ref("region_valid_read_item_tuple"),
        # fixture_ref("block_storage_service_valid_read_item_tuple"),
        # fixture_ref("compute_service_valid_read_item_tuple"),
        # fixture_ref("identity_service_valid_read_item_tuple"),
        # fixture_ref("network_service_valid_read_item_tuple"),
        # fixture_ref("sla_valid_read_item_tuple"),
        # fixture_ref("user_group_valid_read_item_tuple"),
    ],
)
def valid_read_item_tuples(manager, validator, db_item):
    """Parametrized tuple with the items to use in 'case_valid_read_item'."""
    return manager, validator, db_item


@fixture
@parametrize(
    "manager, validator, db_items",
    [
        # fixture_ref("flavor_valid_read_items_tuple"),
        # fixture_ref("identity_provider_valid_read_items_tuple"),
        # fixture_ref("image_valid_read_items_tuple"),
        # fixture_ref("location_valid_read_items_tuple"),
        # fixture_ref("network_valid_read_items_tuple"),
        # fixture_ref("project_valid_read_items_tuple"),
        fixture_ref("provider_valid_read_items_tuple"),
        # fixture_ref("block_storage_quota_valid_read_items_tuple"),
        # fixture_ref("compute_quota_valid_read_items_tuple"),
        # fixture_ref("network_quota_valid_read_items_tuple"),
        # fixture_ref("region_valid_read_items_tuple"),
        # fixture_ref("block_storage_service_valid_read_items_tuple"),
        # fixture_ref("compute_service_valid_read_items_tuple"),
        # fixture_ref("identity_service_valid_read_items_tuple"),
        # fixture_ref("network_service_valid_read_items_tuple"),
        # fixture_ref("sla_valid_read_items_tuple"),
        # fixture_ref("user_group_valid_read_items_tuple"),
    ],
)
def valid_read_items_tuples(manager, validator, db_items):
    """Parametrized tuple with the items to use in 'case_valid_read_item'."""
    return manager, validator, db_items


@fixture
@parametrize(
    "manager, validator, db_item",
    [
        # fixture_ref("flavor_delete_item_tuple"),
        # fixture_ref("identity_provider_delete_item_tuple"),
        # fixture_ref("image_delete_item_tuple"),
        # fixture_ref("location_delete_item_tuple"),
        # fixture_ref("network_delete_item_tuple"),
        # fixture_ref("project_delete_item_tuple"),
        fixture_ref("provider_delete_item_tuple"),
        # fixture_ref("block_storage_quota_delete_item_tuple"),
        # fixture_ref("compute_quota_delete_item_tuple"),
        # fixture_ref("network_quota_delete_item_tuple"),
        # fixture_ref("region_delete_item_tuple"),
        # fixture_ref("block_storage_service_delete_item_tuple"),
        # fixture_ref("compute_service_delete_item_tuple"),
        # fixture_ref("identity_service_delete_item_tuple"),
        # fixture_ref("network_service_delete_item_tuple"),
        # fixture_ref("sla_delete_item_tuple"),
        # fixture_ref("user_group_delete_item_tuple"),
    ],
)
def delete_item_tuples(manager, validator, db_item):
    """Parametrized tuple with the items to use in 'case_delete_item'."""
    return manager, validator, db_item


@fixture
@parametrize(
    "attr",
    [
        # fixture_ref("flavor_attr"),
        # fixture_ref("identity_provider_attr"),
        # fixture_ref("image_attr"),
        # fixture_ref("location_attr"),
        # fixture_ref("network_attr"),
        # fixture_ref("project_attr"),
        fixture_ref("provider_attr"),
        # fixture_ref("block_storage_quota_attr"),
        # fixture_ref("compute_quota_attr"),
        # fixture_ref("network_quota_attr"),
        # fixture_ref("region_attr"),
        # fixture_ref("block_storage_service_attr"),
        # fixture_ref("compute_service_attr"),
        # fixture_ref("identity_service_attr"),
        # fixture_ref("network_service_attr"),
        # fixture_ref("sla_attr"),
        # fixture_ref("user_group_attr"),
    ],
)
def item_attr(attr) -> Optional[str]:
    """Parametrized item attributes."""
    return attr


@fixture
@parametrize(
    "manager",
    [
        # fixture_ref("flavor_manager"),
        # fixture_ref("identity_provider_manager"),
        # fixture_ref("image_manager"),
        # fixture_ref("location_manager"),
        # fixture_ref("network_manager"),
        # fixture_ref("project_manager"),
        fixture_ref("provider_manager"),
        # fixture_ref("block_storage_quota_manager"),
        # fixture_ref("compute_quota_manager"),
        # fixture_ref("network_quota_manager"),
        # fixture_ref("region_manager"),
        # fixture_ref("block_storage_service_manager"),
        # fixture_ref("compute_service_manager"),
        # fixture_ref("identity_service_manager"),
        # fixture_ref("network_service_manager"),
        # fixture_ref("sla_manager"),
        # fixture_ref("user_group_manager"),
    ],
)
def item_manager(manager):
    """Return the manager class."""
    return manager
