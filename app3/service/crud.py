from typing import List, Optional

from . import schemas, models
from ..crud import truncate, update
from ..service_type.schemas import ServiceTypeCreate
from ..service_type.crud import create_service_type, read_service_type


def connect_service_type(
    item: models.Service, type: ServiceTypeCreate
) -> None:
    db_loc = read_service_type(name=type.name)
    if db_loc is None:
        db_loc = create_service_type(type)
    if not item.type.is_connected(db_loc):
        item.type.connect(db_loc)


def create_service(item: schemas.ServiceCreate) -> models.Service:
    db_item = models.Service(**item.dict(exclude={"type"})).save()
    connect_service_type(db_item, item.type)
    return db_item


def read_services(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Service]:
    if kwargs:
        items = models.Service.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Service.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_service(**kwargs) -> Optional[models.Service]:
    return models.Service.nodes.get_or_none(**kwargs)


def remove_service(item: models.Service) -> bool:
    return item.delete()


def edit_service(
    old_item: models.Service, new_item: schemas.ServicePatch
) -> Optional[models.Service]:
    return update(old_item=old_item, new_item=new_item)
