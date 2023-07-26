from uuid import uuid4
from app.flavor.crud import flavor
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorCreate, FlavorUpdate
from app.tests.utils.provider import create_random_provider
from app.tests.utils.utils import (
    random_lower_string,
    random_non_negative_int,
    random_bool,
    random_positive_int,
)


def create_random_flavor() -> Flavor:
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
    return flavor.create(obj_in=item_in, provider=create_random_provider())


def create_random_update_flavor_data() -> FlavorUpdate:
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    num_vcpus = random_non_negative_int()
    num_gpus = random_non_negative_int()
    ram = random_non_negative_int()
    disk = random_non_negative_int()
    infiniband_support = random_bool()
    gpu_model = random_lower_string()
    gpu_vendor = random_lower_string()
    return FlavorUpdate(
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
