from typing import List, Optional
from .. import schemas, models


def create_service(item: schemas.ServiceCreate) -> models.Service:
    return models.Service(**item.dict()).save()


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
    if limit is None:
        return items[skip:]
    return items[skip : skip + limit]


def get_service(**kwargs) -> Optional[models.Service]:
    return models.Service.nodes.get_or_none(**kwargs)


def remove_service(item: models.Service) -> bool:
    return item.delete()


def update_service(
    old_item: models.Service, new_item: schemas.ServiceUpdate
) -> Optional[models.Service]:
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
