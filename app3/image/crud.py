from typing import List, Optional

from . import schemas, models
from ..crud import truncate, update


def create_image(item: schemas.ImageCreate) -> models.Image:
    return models.Image.get_or_create(item.dict())[0]


def read_images(
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


def read_image(**kwargs) -> Optional[models.Image]:
    return models.Image.nodes.get_or_none(**kwargs)


def remove_image(item: models.Image) -> bool:
    return item.delete()


def edit_image(
    old_item: models.Image, new_item: schemas.ImagePatch
) -> Optional[models.Image]:
    return update(old_item=old_item, new_item=new_item)
