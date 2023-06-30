from typing import Generator

from ..utils.flavor import create_random_flavor
from ..utils.utils import (
    random_lower_string,
    random_non_negative_int,
    random_bool,
)
from ...flavor.crud import flavor
from ...flavor.schemas import FlavorCreate, FlavorUpdate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    num_vcpus = random_non_negative_int()
    num_gpus = random_non_negative_int()
    ram = random_non_negative_int()
    disk = random_non_negative_int()
    infiniband_support = random_bool()
    gpu_model = random_lower_string()
    gpu_vendor = random_lower_string()
    item_in = FlavorCreate(
        description=description,
        num_vcpus=num_vcpus,
        num_gpus=num_gpus,
        ram=ram,
        disk=disk,
        infiniband_support=infiniband_support,
        gpu_model=gpu_model,
        gpu_vendor=gpu_vendor,
    )
    item = flavor.create(obj_in=item_in)
    assert item.description == description
    assert item.num_vcpus == num_vcpus
    assert item.num_gpus == num_gpus
    assert item.ram == ram
    assert item.disk == disk
    assert item.infiniband_support == infiniband_support
    assert item.gpu_model == gpu_model
    assert item.gpu_vendor == gpu_vendor


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    item_in = FlavorCreate(name=name)
    item = flavor.create(obj_in=item_in)
    assert item.description == ""
    assert item.num_vcpus == 0
    assert item.num_gpus == 0
    assert item.ram == 0
    assert item.disk == 0
    assert item.infiniband_support is False
    assert item.gpu_model is None
    assert item.gpu_vendor is None


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_flavor()
    stored_item = flavor.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.num_vcpus == stored_item.num_vcpus
    assert item.num_gpus == stored_item.num_gpus
    assert item.ram == stored_item.ram
    assert item.disk == stored_item.disk
    assert item.infiniband_support == stored_item.infiniband_support
    assert item.gpu_model == stored_item.gpu_model
    assert item.gpu_vendor == stored_item.gpu_vendor


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_flavor()
    description2 = random_lower_string()
    num_vcpus2 = random_non_negative_int()
    num_gpus2 = random_non_negative_int()
    ram2 = random_non_negative_int()
    disk2 = random_non_negative_int()
    infiniband_support2 = not item.infiniband_support
    gpu_model2 = random_lower_string()
    gpu_vendor2 = random_lower_string()
    item_update = FlavorUpdate(
        description=description2,
        num_vcpus=num_vcpus2,
        num_gpus=num_gpus2,
        ram=ram2,
        disk=disk2,
        infiniband_support=infiniband_support2,
        gpu_model=gpu_model2,
        gpu_vendor=gpu_vendor2,
    )
    item2 = flavor.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == description2
    assert item2.num_vcpus == num_vcpus2
    assert item2.num_gpus == num_gpus2
    assert item2.ram == ram2
    assert item2.disk == disk2
    assert item2.infiniband_support == infiniband_support2
    assert item2.gpu_model == gpu_model2
    assert item2.gpu_vendor == gpu_vendor2


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_flavor()
    item2 = flavor.remove(db_obj=item)
    item3 = flavor.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
