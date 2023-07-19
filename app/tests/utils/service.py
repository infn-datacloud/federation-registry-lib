from random import choice

from app.service.crud import service
from app.service.enum import ServiceType
from app.service.models import Service
from app.service.schemas import ServiceCreate, ServiceUpdate
from app.tests.utils.utils import random_lower_string, random_url


def create_random_service() -> Service:
    description = random_lower_string()
    endpoint = random_url()
    item_in = ServiceCreate(description=description, endpoint=endpoint)
    return service.create(obj_in=item_in)


def create_random_update_service_data() -> ServiceUpdate:
    description = random_lower_string()
    endpoint = random_url()
    return ServiceUpdate(description=description, endpoint=endpoint)

def random_service_type() -> str:
    return choice([i.value for i in ServiceType])