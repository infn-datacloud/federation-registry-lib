from random import choice

from .utils import random_lower_string
from ...service_type.crud import service_type
from ...service_type.enum import ServiceType as ServiceTypeEnum
from ...service_type.models import ServiceType
from ...service_type.schemas import ServiceTypeCreate, ServiceTypeUpdate


def create_random_service_type() -> ServiceType:
    description = random_lower_string()
    name = random_name()
    item_in = ServiceTypeCreate(name=name, description=description)
    return service_type.create(obj_in=item_in)


def create_random_update_service_type_data() -> ServiceTypeUpdate:
    description = random_lower_string()
    name = random_name()
    return ServiceTypeUpdate(name=name, description=description)


def random_name() -> str:
    return choice([i.value for i in ServiceTypeEnum])
