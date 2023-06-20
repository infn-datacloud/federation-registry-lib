from typing import List, Optional

from .utils import truncate, update
from .. import schemas, models


def create_location(item: schemas.LocationCreate) -> models.Location:
    return models.Location(**item.dict()).save()


def read_locations(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Location]:
    if kwargs:
        items = models.Location.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Location.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_location(**kwargs) -> Optional[models.Location]:
    return models.Location.nodes.get_or_none(**kwargs)


def remove_location(item: models.Location) -> bool:
    return item.delete()


def edit_location(
    old_item: models.Location, new_item: schemas.LocationPatch
) -> Optional[models.Location]:
    return update(old_item=old_item, new_item=new_item)
