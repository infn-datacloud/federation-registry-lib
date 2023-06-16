from typing import List, Optional
from .. import schemas, models


def create_provider(item: schemas.ProviderCreate) -> models.Provider:
    return models.Provider(**item.dict()).save()


def get_providers(
    skip: int = 0, limit: int = 100, sort: Optional[str] = None, **kwargs
) -> List[schemas.Provider]:
    if kwargs:
        items = models.Provider.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Provider.nodes.order_by(sort).all()
    return items[skip : skip + limit]


def get_provider(**kwargs) -> Optional[schemas.Provider]:
    return models.Provider.nodes.get_or_none(**kwargs)


def remove_provider(item: models.Provider) -> bool:
    return item.delete()


def update_provider(
    old_item: models.Provider, new_item: schemas.ProviderUpdate
) -> Optional[schemas.Provider]:
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
