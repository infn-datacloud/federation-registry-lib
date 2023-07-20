from typing import Generator
from uuid import uuid4
from app.image.crud import image
from app.image.schemas import ImageCreate
from app.tests.utils.image import (
    create_random_image,
    create_random_update_image_data,
    random_os,
)
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import (
    random_lower_string,
    random_bool,
    random_datetime,
)


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    os = random_os()
    distribution = random_lower_string()
    version = random_lower_string()
    architecture = random_lower_string()
    cuda_support = random_bool()
    gpu_driver = random_bool()
    creation_time = random_datetime()
    item_in = ImageCreate(
        description=description,
        name=name,
        uuid=uuid,
        os=os,
        distribution=distribution,
        version=version,
        architecture=architecture,
        cuda_support=cuda_support,
        gpu_driver=gpu_driver,
        creation_time=creation_time,
    )
    item = image.create(obj_in=item_in, provider=create_random_provider())
    assert item.description == description
    assert item.name == name
    assert item.uuid == str(uuid)
    assert item.os == os
    assert item.distribution == distribution
    assert item.version == version
    assert item.architecture == architecture
    assert item.cuda_support == cuda_support
    assert item.gpu_driver == gpu_driver
    assert item.creation_time == creation_time


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    name = random_lower_string()
    uuid = uuid4()
    os = random_os()
    distribution = random_lower_string()
    version = random_lower_string()
    architecture = random_lower_string()
    item_in = ImageCreate(
        name=name,
        uuid=uuid,
        os=os,
        distribution=distribution,
        version=version,
        architecture=architecture,
    )
    item = image.create(obj_in=item_in, provider=create_random_provider())
    assert item.description == ""
    assert item.name == name
    assert item.uuid == str(uuid)
    assert item.os == os
    assert item.distribution == distribution
    assert item.version == version
    assert item.architecture == architecture
    assert item.cuda_support is False
    assert item.gpu_driver is False
    assert item.creation_time is None


def test_get_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_image()
    stored_item = image.get(uid=item.uid)
    assert stored_item
    assert item.uid == stored_item.uid
    assert item.description == stored_item.description
    assert item.name == stored_item.name
    assert item.uuid == stored_item.uuid
    assert item.os == stored_item.os
    assert item.distribution == stored_item.distribution
    assert item.version == stored_item.version
    assert item.architecture == stored_item.architecture
    assert item.cuda_support == stored_item.cuda_support
    assert item.gpu_driver == stored_item.gpu_driver
    assert item.creation_time == stored_item.creation_time


def test_get_items(setup_and_teardown_db: Generator) -> None:
    item = create_random_image()
    item2 = create_random_image()
    stored_items = image.get_multi()
    assert len(stored_items) == 2

    stored_items = image.get_multi(limit=1)
    assert len(stored_items) == 1

    stored_items = image.get_multi(uid=item.uid)
    assert len(stored_items) == 1
    assert stored_items[0].uid == item.uid
    assert stored_items[0].description == item.description
    assert stored_items[0].name == item.name
    assert stored_items[0].uuid == item.uuid
    assert stored_items[0].os == item.os
    assert stored_items[0].distribution == item.distribution
    assert stored_items[0].version == item.version
    assert stored_items[0].architecture == item.architecture
    assert stored_items[0].cuda_support == item.cuda_support
    assert stored_items[0].gpu_driver == item.gpu_driver
    assert stored_items[0].creation_time == item.creation_time

    sorted_items = list(sorted([item, item2], key=lambda x: x.uid))
    stored_items = image.get_multi(sort="uid")
    assert stored_items[0].uid == sorted_items[0].uid
    assert stored_items[1].uid == sorted_items[1].uid
    stored_items = image.get_multi(sort="-uid")
    assert stored_items[0].uid == sorted_items[1].uid
    assert stored_items[1].uid == sorted_items[0].uid


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_image()
    item_update = create_random_update_image_data()
    item2 = image.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.os == item_update.os
    assert item2.distribution == item_update.distribution
    assert item2.version == item_update.version
    assert item2.architecture == item_update.architecture
    assert item2.cuda_support == item_update.cuda_support
    assert item2.gpu_driver == item_update.gpu_driver
    assert item2.creation_time == item_update.creation_time

    item_update = create_random_update_image_data()
    item2 = image.update(db_obj=item, obj_in=item_update.dict())
    assert item2.uid == item.uid
    assert item2.description == item_update.description
    assert item2.os == item_update.os
    assert item2.distribution == item_update.distribution
    assert item2.version == item_update.version
    assert item2.architecture == item_update.architecture
    assert item2.cuda_support == item_update.cuda_support
    assert item2.gpu_driver == item_update.gpu_driver
    assert item2.creation_time == item_update.creation_time


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_image()
    item2 = image.remove(db_obj=item)
    item3 = image.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
