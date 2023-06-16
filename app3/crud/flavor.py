from typing import List, Optional
from .. import schemas, models


def create_flavor(item: schemas.FlavorCreate) -> models.Flavor:
    return models.Flavor(**item.dict()).save()


def get_flavors(
    skip: int = 0, limit: int = 100, sort: Optional[str] = None, **kwargs
) -> List[models.Flavor]:
    if kwargs:
        items = models.Flavor.nodes.filter(**kwargs).order_by(sort).all()
        print(kwargs)
    else:
        items = models.Flavor.nodes.order_by(sort).all()
    return items[skip : skip + limit]


def get_flavor(**kwargs) -> Optional[models.Flavor]:
    return models.Flavor.nodes.get_or_none(**kwargs)


def remove_flavor(item: models.Flavor) -> bool:
    return item.delete()


def update_flavor(
    old_item: models.Flavor, new_item: schemas.FlavorUpdate
) -> Optional[models.Flavor]:
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
