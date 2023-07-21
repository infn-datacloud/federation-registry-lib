from typing import Generator
from uuid import uuid4
from app.flavor.crud import flavor
from app.flavor.schemas import FlavorCreate
from app.tests.utils.flavor import (
    create_random_flavor,
    create_random_update_flavor_data,
)
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import (
    random_lower_string,
    random_non_negative_int,
    random_bool,
    random_positive_int,
)


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    num_vcpus = random_non_negative_int()
    num_gpus = random_positive_int()
    ram = random_non_negative_int()
    disk = random_non_negative_int()
    infiniband_support = random_bool()
    gpu_model = random_lower_string()
    gpu_vendor = random_lower_string()
    item_in = FlavorCreate(
        description=description,
        name=name,
        uuid=uuid,
        num_vcpus=num_vcpus,
        num_gpus=num_gpus,
        ram=ram,
        disk=disk,
        infiniband_support=infiniband_support,
        gpu_model=gpu_model,
        gpu_vendor=gpu_vendor,
    )
    provider = create_random_provider()
    item = flavor.create(obj_in=item_in, provider=provider)
    assert item.description == description
    assert item.name == name
    assert item.uuid == str(uuid)
    assert item.num_vcpus == num_vcpus
    assert item.num_gpus == num_gpus
    assert item.ram == ram
    assert item.disk == disk
    assert item.infiniband_support == infiniband_support
    assert item.gpu_model == gpu_model
    assert item.gpu_vendor == gpu_vendor
    item_provider = item.provider.single()
    assert item_provider is not None
    assert item_provider.uid == provider.uid


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    uuid = uuid4()
    provider = create_random_provider()
    item_in = FlavorCreate(name=name, uuid=uuid)
    item = flavor.create(obj_in=item_in, provider=provider)
    assert item.description == ""
    assert item.name == name
    assert item.uuid == str(uuid)
    assert item.num_vcpus == 0
    assert item.num_gpus == 0
    assert item.ram == 0
    assert item.disk == 0
    assert item.infiniband_support is False
    assert item.gpu_model is None
    assert item.gpu_vendor is None
    item_provider = item.provider.single()
    assert item_provider is not None
    assert item_provider.uid == provider.uid


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_flavor()
    stored_item = flavor.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.name == stored_item.name
    assert item.uuid == stored_item.uuid
    assert item.description == stored_item.description
    assert item.num_vcpus == stored_item.num_vcpus
    assert item.num_gpus == stored_item.num_gpus
    assert item.ram == stored_item.ram
    assert item.disk == stored_item.disk
    assert item.infiniband_support == stored_item.infiniband_support
    assert item.gpu_model == stored_item.gpu_model
    assert item.gpu_vendor == stored_item.gpu_vendor


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_flavor()
    item2 = create_random_flavor()
    stored_items = flavor.get_multi()
    assert len(stored_items) == 2

    stored_items = flavor.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = flavor.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].name == item.name
    assert stored_items[0].uuid == item.uuid
    assert stored_items[0].num_vcpus == item.num_vcpus
    assert stored_items[0].num_gpus == item.num_gpus
    assert stored_items[0].ram == item.ram
    assert stored_items[0].disk == item.disk
    assert stored_items[0].infiniband_support == item.infiniband_support
    assert stored_items[0].gpu_model == item.gpu_model
    assert stored_items[0].gpu_vendor == item.gpu_vendor

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = flavor.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = flavor.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_flavor()
    item_update = create_random_update_flavor_data()
    item2 = flavor.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.num_vcpus == item_update.num_vcpus
    assert item2.num_gpus == item_update.num_gpus
    assert item2.ram == item_update.ram
    assert item2.disk == item_update.disk
    assert item2.infiniband_support == item_update.infiniband_support
    assert item2.gpu_model == item_update.gpu_model
    assert item2.gpu_vendor == item_update.gpu_vendor

    item_update = create_random_update_flavor_data()
    item2 = flavor.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.num_vcpus == item_update.num_vcpus
    assert item2.num_gpus == item_update.num_gpus
    assert item2.ram == item_update.ram
    assert item2.disk == item_update.disk
    assert item2.infiniband_support == item_update.infiniband_support
    assert item2.gpu_model == item_update.gpu_model
    assert item2.gpu_vendor == item_update.gpu_vendor


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_flavor()
    item2 = flavor.remove(db_obj=item)
    item3 = flavor.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
