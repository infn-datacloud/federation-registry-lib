from typing import List, Optional

from .quota_type import create_quota_type, get_quota_type
from .utils import truncate, update
from .. import schemas, models


def connect_service_type_to_quota_types(
    item: models.ServiceType, types: List[schemas.QuotaTypeCreate]
) -> None:
    for type in types:
        db_qt = get_quota_type(name=type.name)
        if db_qt is None:
            db_qt = create_quota_type(type)
        if not item.quota_types.is_connected(db_qt):
            item.quota_types.connect(db_qt)


def create_service_type(item: schemas.ServiceTypeCreate) -> models.ServiceType:
    db_item = models.ServiceType(**item.dict(exclude={"quota_types"})).save()
    connect_service_type_to_quota_types(db_item, item.quota_types)
    return db_item


def get_service_types(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.ServiceType]:
    if kwargs:
        items = models.ServiceType.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.ServiceType.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def get_service_type(**kwargs) -> Optional[models.ServiceType]:
    return models.ServiceType.nodes.get_or_none(**kwargs)


def remove_service_type(item: models.ServiceType) -> bool:
    return item.delete()


def update_service_type(
    old_item: models.ServiceType, new_item: schemas.ServiceTypeUpdate
) -> Optional[models.ServiceType]:
    return update(old_item=old_item, new_item=new_item)
