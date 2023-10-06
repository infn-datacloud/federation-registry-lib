from typing import Generator
from uuid import uuid4

from app.provider.crud import provider
from app.service.enum import ServiceType
from app.tests.utils.provider import create_random_provider, validate_provider_attrs


def test_create_item(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(default=True)
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(with_projects=True)
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_identity_providers(
    setup_and_teardown_db: Generator,
) -> None:
    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_projects_and_regions(
    setup_and_teardown_db: Generator,
) -> None:
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_everything(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(
        with_projects=True, with_identity_providers=True, with_regions=True
    )
    item = provider.create(obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_create_item_with_identity_providers(
    setup_and_teardown_db: Generator,
) -> None:
    item_in = create_random_provider(with_identity_providers=True)
    item = provider.create(obj_in=item_in)
    assert len(item.identity_providers) == len(item_in.identity_providers)
    for db_idp, idp_in in zip(item.identity_providers, item_in.identity_providers):
        assert len(db_idp.user_groups) == len(idp_in.user_groups)
        for db_group in db_idp.user_groups:
            assert len(db_group.slas) == 0


def test_create_item_with_regions(
    setup_and_teardown_db: Generator,
) -> None:
    item_in = create_random_provider(with_regions=True)
    item = provider.create(obj_in=item_in)
    assert len(item.regions) == len(item_in.regions)
    for db_reg, reg_in in zip(item.regions, item_in.regions):
        db_block_storage_services = list(
            filter(lambda x: x.type == ServiceType.BLOCK_STORAGE.value, db_reg.services)
        )
        assert len(db_block_storage_services) == len(reg_in.block_storage_services)
        for db_serv in db_block_storage_services:
            assert len(db_serv.quotas) == 0
        db_compute_services = list(
            filter(lambda x: x.type == ServiceType.COMPUTE.value, db_reg.services)
        )
        assert len(db_compute_services) == len(reg_in.compute_services)
        for db_serv in db_compute_services:
            assert len(db_serv.quotas) == 0


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item = provider.get(uid=item.uid)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_get_non_existing_item(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item = provider.get(uid=uuid4())
    assert not item


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item_in2 = create_random_provider()
    item2 = provider.create(obj_in=item_in2)

    stored_items = provider.get_multi()
    assert len(stored_items) == 2

    stored_items = provider.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    validate_provider_attrs(obj_in=item_in, db_item=stored_items[0])

    stored_items = provider.get_multi(uid=item2.uid)
    assert len(stored_items) == 1
    validate_provider_attrs(obj_in=item_in2, db_item=stored_items[0])


def test_get_items_with_limit(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    provider.create(obj_in=item_in)
    item_in2 = create_random_provider()
    provider.create(obj_in=item_in2)

    stored_items = provider.get_multi(limit=0)
    assert len(stored_items) == 0

    stored_items = provider.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = provider.get_multi(limit=None)
    assert len(stored_items) == 2


def test_get_sorted_items(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item_in2 = create_random_provider()
    item2 = provider.create(obj_in=item_in2)

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))

    stored_items = provider.get_multi(sort="uid")
    assert sorted_items[0].uid == stored_items[0].uid
    assert sorted_items[1].uid == stored_items[1].uid

    stored_items = provider.get_multi(sort="-uid")
    assert sorted_items[1].uid == stored_items[0].uid
    assert sorted_items[0].uid == stored_items[1].uid


def test_get_items_with_skip(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    provider.create(obj_in=item_in)
    item_in2 = create_random_provider()
    provider.create(obj_in=item_in2)

    stored_items = provider.get_multi(skip=0)
    assert len(stored_items) == 2

    stored_items = provider.get_multi(skip=1)
    assert len(stored_items) == 1


def test_patch_item(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider()
    item = provider.update(db_obj=item, obj_in=item_in)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(with_projects=True)
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider()
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    projects = item_in.projects
    item_in = create_random_provider()
    item_in.projects = projects
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_identity_providers(
    setup_and_teardown_db: Generator,
) -> None:
    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider()
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True, with_identity_providers=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    projects = item_in.projects
    identity_providers = item_in.identity_providers
    item_in = create_random_provider()
    item_in.projects = projects
    item_in.identity_providers = identity_providers
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_forced_update_item_with_projects_and_regions(
    setup_and_teardown_db: Generator,
) -> None:
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    item_in = create_random_provider(with_projects=True, with_regions=True)
    item = provider.create(obj_in=item_in)
    item_in = create_random_provider()
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)

    projects = item_in.projects
    regions = item_in.regions
    item_in = create_random_provider()
    item_in.projects = projects
    item_in.regions = regions
    item = provider.update(db_obj=item, obj_in=item_in, force=True)
    validate_provider_attrs(obj_in=item_in, db_item=item)


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider()
    item = provider.create(obj_in=item_in)
    result = provider.remove(db_obj=item)
    assert result
    item = provider.get(uid=item.uid)
    assert not item


def test_delete_item_with_relationships(setup_and_teardown_db: Generator) -> None:
    item_in = create_random_provider(
        with_identity_providers=True, with_projects=True, with_regions=True
    )
    item = provider.create(obj_in=item_in)
    result = provider.remove(db_obj=item)
    assert result
    item = provider.get(uid=item.uid)
    assert not item
