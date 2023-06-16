from typing import List, Optional

from .location import create_location, get_location
from .. import schemas, models


def connect_provider_to_location(
    item: models.Provider, location: schemas.LocationCreate
) -> None:
    db_loc = get_location(**location.dict(exclude_unset=True))
    if db_loc is None:
        db_loc = create_location(location)
    item.location.connect(db_loc)


def create_provider(item: schemas.ProviderCreate) -> models.Provider:
    db_item = models.Provider(**item.dict(exclude={"location"})).save()
    if item.location is not None:
        connect_provider_to_location(db_item, item.location)
    return db_item


def get_providers(
    skip: int = 0, limit: int = 100, sort: Optional[str] = None, **kwargs
) -> List[models.Provider]:
    if kwargs:
        items = models.Provider.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Provider.nodes.order_by(sort).all()
    return items[skip : skip + limit]


def get_provider(**kwargs) -> Optional[models.Provider]:
    return models.Provider.nodes.get_or_none(**kwargs)


def remove_provider(item: models.Provider) -> bool:
    return item.delete()


def update_provider(
    old_item: models.Provider, new_item: schemas.ProviderUpdate
) -> Optional[models.Provider]:
    for k, v in new_item.dict(
        exclude={"location"}, exclude_unset=True
    ).items():
        old_item.__setattr__(k, v)
    connect_provider_to_location(old_item, new_item.location)
    old_item.save()
    return old_item
