from .utils import random_lower_string, random_url
from ...service.crud import service
from ...service.models import Service
from ...service.schemas import ServiceCreate


def create_random_service() -> Service:
    description = random_lower_string()
    endpoint = random_url()
    item_in = ServiceCreate(description=description, endpoint=endpoint)
    return service.create(obj_in=item_in)
