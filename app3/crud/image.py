from typing import List, Optional
from .. import schemas, models


def create_image(item: schemas.ImageCreate) -> models.Image:
    return models.Image(**item.dict()).save()


def get_images(
    skip: int = 0, limit: Optional[int] = None, sort: Optional[str] = None, **kwargs
) -> List[models.Image]:
    if kwargs:
        items = models.Image.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Image.nodes.order_by(sort).all()
    if limit is None:
        return items[skip:]
    return items[skip : skip + limit]


def get_image(**kwargs) -> Optional[models.Image]:
    return models.Image.nodes.get_or_none(**kwargs)


def remove_image(item: models.Image) -> bool:
    return item.delete()


def update_image(
    old_item: models.Image, new_item: schemas.ImageUpdate
) -> Optional[models.Image]:
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
