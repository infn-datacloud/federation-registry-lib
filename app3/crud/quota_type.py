from typing import List, Optional

from .utils import truncate, update
from .. import schemas, models


def create_quota_type(item: schemas.QuotaTypeCreate) -> models.QuotaType:
    return models.QuotaType(**item.dict()).save()


def read_quota_types(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.QuotaType]:
    if kwargs:
        items = models.QuotaType.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.QuotaType.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_quota_type(**kwargs) -> Optional[models.QuotaType]:
    return models.QuotaType.nodes.get_or_none(**kwargs)


def remove_quota_type(item: models.QuotaType) -> bool:
    return item.delete()


def edit_quota_type(
    old_item: models.QuotaType, new_item: schemas.QuotaTypePatch
) -> Optional[models.QuotaType]:
    return update(old_item=old_item, new_item=new_item)
