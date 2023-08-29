from random import choice
from uuid import uuid4

from app.image.crud import image
from app.image.enum import ImageOS
from app.image.models import Image
from app.image.schemas import ImageCreate, ImageUpdate
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import random_bool, random_datetime, random_lower_string


def create_random_image() -> Image:
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
    return image.create(obj_in=item_in, provider=create_random_provider())


def create_random_update_image_data() -> ImageUpdate:
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
    return ImageUpdate(
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


def random_os() -> str:
    return choice([i.value for i in ImageOS])
