from .utils import random_lower_string, random_non_negative_int, random_bool
from ...flavor.crud import flavor
from ...flavor.models import Flavor
from ...flavor.schemas import FlavorCreate


def create_random_flavor() -> Flavor:
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
    return flavor.create(obj_in=item_in)
