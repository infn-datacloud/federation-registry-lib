from typing import List, Optional
from .. import schemas, models


def create_service(item: schemas.ServiceCreate) -> schemas.Service:
    return models.Service(**item.dict()).save()


def get_services(**kwargs) -> List[schemas.Service]:
    if kwargs:
        return models.Service.nodes.filter(**kwargs).all()
    return models.Service.nodes.all()


def get_service(**kwargs) -> Optional[schemas.Service]:
    return models.Service.nodes.get_or_none(**kwargs)


def remove_service(item: models.Service) -> bool:
    return item.delete()


def connect_service_to_sla(sla: models.SLA, service: models.Service) -> bool:
    return service.sla.connect(sla)
