from random import choice

from .utils import random_lower_string, random_bool, random_datetime
from ...image.crud import image
from ...image.models import Image
from ...image.schemas import ImageCreate
from ...image.enum import ImageOS


def create_random_image() -> Image:
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
    return image.create(obj_in=item_in)


def random_os() -> str:
    return choice([i.value for i in ImageOS])
