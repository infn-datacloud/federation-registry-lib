from typing import List, Optional

from .utils import truncate, update
from .. import schemas, models


def create_image(item: schemas.ImageCreate) -> models.Image:
    return models.Image(**item.dict()).save()


def get_images(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Image]:
    if kwargs:
        items = models.Image.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Image.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def get_image(**kwargs) -> Optional[models.Image]:
    return models.Image.nodes.get_or_none(**kwargs)


def remove_image(item: models.Image) -> bool:
    return item.delete()


def update_image(
    old_item: models.Image, new_item: schemas.ImageUpdate
) -> Optional[models.Image]:
    return update(old_item=old_item, new_item=new_item)
