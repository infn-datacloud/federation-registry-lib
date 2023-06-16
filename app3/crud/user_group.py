from typing import List, Optional
from .. import schemas, models


def create_user_group(item: schemas.UserGroupCreate) -> models.UserGroup:
    return models.UserGroup(**item.dict()).save()


def get_user_groups(
    skip: int = 0, limit: Optional[int] = None, sort: Optional[str] = None, **kwargs
) -> List[models.UserGroup]:
    if kwargs:
        items = models.UserGroup.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.UserGroup.nodes.order_by(sort).all()
    if limit is None:
        return items[skip:]
    return items[skip : skip + limit]


def get_user_group(**kwargs) -> Optional[models.UserGroup]:
    return models.UserGroup.nodes.get_or_none(**kwargs)


def remove_user_group(item: models.UserGroup) -> bool:
    return item.delete()


def update_user_group(
    old_item: models.UserGroup, new_item: schemas.UserGroupUpdate
) -> Optional[models.UserGroup]:
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
