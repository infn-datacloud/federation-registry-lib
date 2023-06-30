from typing import Generator

from ..utils.image import create_random_image, random_os
from ..utils.utils import random_lower_string, random_bool, random_datetime
from ...image.crud import image
from ...image.schemas import ImageCreate, ImageUpdate


def test_create_item(setup_and_teardown_db: Generator) -> None:
    description = random_lower_string()
    os = random_os()
    distribution = random_lower_string()
    version = random_lower_string()
    architecture = random_lower_string()
    cuda_support = random_bool()
    gpu_driver = random_bool()
    creation_time = random_datetime()
    item_in = ImageCreate(
        description=description,
        os=os,
        distribution=distribution,
        version=version,
        architecture=architecture,
        cuda_support=cuda_support,
        gpu_driver=gpu_driver,
        creation_time=creation_time,
    )
    item = image.create(obj_in=item_in)
    assert item.description == description
    assert item.os == os
    assert item.distribution == distribution
    assert item.version == version
    assert item.architecture == architecture
    assert item.cuda_support == cuda_support
    assert item.gpu_driver == gpu_driver
    assert item.creation_time == creation_time


def test_create_item_default_values(setup_and_teardown_db: Generator) -> None:
    os = random_os()
    distribution = random_lower_string()
    version = random_lower_string()
    architecture = random_lower_string()
    item_in = ImageCreate(
        os=os,
        distribution=distribution,
        version=version,
        architecture=architecture,
    )
    item = image.create(obj_in=item_in)
    assert item.description == ""
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
    assert item.os == stored_item.os
    assert item.distribution == stored_item.distribution
    assert item.version == stored_item.version
    assert item.architecture == stored_item.architecture
    assert item.cuda_support == stored_item.cuda_support
    assert item.gpu_driver == stored_item.gpu_driver
    assert item.creation_time == stored_item.creation_time


def test_update_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_image()
    description2 = random_lower_string()
    os2 = random_os()
    distribution2 = random_lower_string()
    version2 = random_lower_string()
    architecture2 = random_lower_string()
    cuda_support2 = not item.cuda_support
    gpu_driver2 = not item.gpu_driver
    creation_time2 = random_datetime()

    item_update = ImageUpdate(
        description=description2,
        os=os2,
        distribution=distribution2,
        version=version2,
        architecture=architecture2,
        cuda_support=cuda_support2,
        gpu_driver=gpu_driver2,
        creation_time=creation_time2,
    )
    item2 = image.update(db_obj=item, obj_in=item_update)
    assert item2.uid == item.uid
    assert item2.description == description2
    assert item2.os == os2
    assert item2.distribution == distribution2
    assert item2.version == version2
    assert item2.architecture == architecture2
    assert item2.cuda_support == cuda_support2
    assert item2.gpu_driver == gpu_driver2
    assert item2.creation_time == creation_time2


def test_delete_item(setup_and_teardown_db: Generator) -> None:
    item = create_random_image()
    item2 = image.remove(db_obj=item)
    item3 = image.get(uid=item.uid)
    assert item2 is True
    assert item3 is None
