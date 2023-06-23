from typing import List, Optional

from . import schemas, models
from ..crud import truncate, update


def create_flavor(item: schemas.FlavorCreate) -> models.Flavor:
    return models.Flavor.get_or_create(item.dict())[0]


def read_flavors(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Flavor]:
    if kwargs:
        items = models.Flavor.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Flavor.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_flavor(**kwargs) -> Optional[models.Flavor]:
    return models.Flavor.nodes.get_or_none(**kwargs)


def remove_flavor(item: models.Flavor) -> bool:
    return item.delete()


def edit_flavor(
    old_item: models.Flavor, new_item: schemas.FlavorPatch
) -> Optional[models.Flavor]:
    return update(old_item=old_item, new_item=new_item)
