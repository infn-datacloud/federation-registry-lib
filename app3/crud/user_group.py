from typing import List, Optional
from .. import schemas, models


def create_user_group(item: schemas.UserGroupCreate) -> schemas.UserGroup:
    return models.UserGroup(**item.dict()).save()


def get_user_groups(**kwargs) -> List[schemas.UserGroup]:
    if kwargs:
        return models.UserGroup.nodes.filter(**kwargs).all()
    return models.UserGroup.nodes.all()


def get_user_group(**kwargs) -> Optional[schemas.UserGroup]:
    return models.UserGroup.nodes.get_or_none(**kwargs)


def remove_user_group(item: models.UserGroup) -> bool:
    return item.delete()
