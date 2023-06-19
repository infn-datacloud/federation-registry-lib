from typing import List, Optional

from .utils import truncate, update
from .. import schemas, models


def create_user_group(item: schemas.UserGroupCreate) -> models.UserGroup:
    return models.UserGroup(**item.dict()).save()


def get_user_groups(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.UserGroup]:
    if kwargs:
        items = models.UserGroup.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.UserGroup.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def get_user_group(**kwargs) -> Optional[models.UserGroup]:
    return models.UserGroup.nodes.get_or_none(**kwargs)


def remove_user_group(item: models.UserGroup) -> bool:
    return item.delete()


def update_user_group(
    old_item: models.UserGroup, new_item: schemas.UserGroupUpdate
) -> Optional[models.UserGroup]:
    return update(old_item=old_item, new_item=new_item)
