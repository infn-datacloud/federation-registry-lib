from typing import List, Optional

from . import schemas, models
from ..crud import truncate, update


def create_identity_provider(
    item: schemas.IdentityProviderCreate,
) -> models.IdentityProvider:
    return models.IdentityProvider.get_or_create(item.dict())[0]


def read_identity_providers(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.IdentityProvider]:
    if kwargs:
        items = (
            models.IdentityProvider.nodes.filter(**kwargs).order_by(sort).all()
        )
    else:
        items = models.IdentityProvider.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_identity_provider(**kwargs) -> Optional[models.IdentityProvider]:
    return models.IdentityProvider.nodes.get_or_none(**kwargs)


def remove_identity_provider(item: models.IdentityProvider) -> bool:
    return item.delete()


def edit_identity_provider(
    old_item: models.IdentityProvider, new_item: schemas.IdentityProviderPatch
) -> Optional[models.IdentityProvider]:
    return update(old_item=old_item, new_item=new_item)
