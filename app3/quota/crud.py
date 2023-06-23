from typing import List, Optional

from . import schemas, models
from ..quota_type.crud import create_quota_type, read_quota_type
from ..service.crud import read_service
from ..crud import truncate, update


def connect_quota_to_service(
    item: models.Quota, service: schemas.ServiceCreate
) -> None:
    db_srv = read_service(endpoint=service.endpoint)
    if db_srv is None:
        pass # TODO  raise error -> elevate logic in router
    if not item.service.is_connected(db_srv):
        item.service.connect(db_srv)


def connect_quota_type(
    item: models.Quota, type: schemas.QuotaTypeCreate
) -> None:
    db_type = read_quota_type(name=type.name)
    if db_type is None:
        db_type = create_quota_type(type)
    if not item.type.is_connected(db_type):
        item.type.connect(db_type)


def create_quota(item: schemas.QuotaCreate) -> models.Quota:
    db_item = models.Quota(**item.dict(exclude={"type", "service"})).save()
    connect_quota_type(db_item, item.type)
    connect_quota_to_service(db_item, item.service)
    return db_item


def read_quotas(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Quota]:
    if kwargs:
        items = models.Quota.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Quota.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_quota(**kwargs) -> Optional[models.Quota]:
    return models.Quota.nodes.get_or_none(**kwargs)


def remove_quota(item: models.Quota) -> bool:
    return item.delete()


def edit_quota(
    old_item: models.Quota, new_item: schemas.QuotaPatch
) -> Optional[models.Quota]:
    return update(old_item=old_item, new_item=new_item)
