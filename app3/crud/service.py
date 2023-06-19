from typing import List, Optional

from .service_type import create_service_type, get_service_type
from .utils import truncate, update
from .. import schemas, models


def connect_service_type(
    item: models.Service, type: schemas.ServiceTypeCreate
) -> None:
    db_loc = get_service_type(name=type.name)
    if db_loc is None:
        db_loc = create_service_type(type)
    if not item.type.is_connected(db_loc):
        item.type.connect(db_loc)


def create_service(item: schemas.ServiceCreate) -> models.Service:
    db_item = models.Service(**item.dict(exclude={"type"})).save()
    connect_service_type(db_item, item.type)
    return db_item


def get_services(
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


def get_service(**kwargs) -> Optional[models.Service]:
    return models.Service.nodes.get_or_none(**kwargs)


def remove_service(item: models.Service) -> bool:
    return item.delete()


def update_service(
    old_item: models.Service, new_item: schemas.ServiceUpdate
) -> Optional[models.Service]:
    return update(old_item=old_item, new_item=new_item)
