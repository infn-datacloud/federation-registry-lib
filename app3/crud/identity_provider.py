from typing import List, Optional
from .. import schemas, models


def create_identity_provider(
    item: schemas.IdentityProviderCreate,
) -> models.IdentityProvider:
    return models.IdentityProvider(**item.dict()).save()


def get_identity_providers(
    skip: int = 0, limit: Optional[int] = None, sort: Optional[str] = None, **kwargs
) -> List[models.IdentityProvider]:
    if kwargs:
        items = (
            models.IdentityProvider.nodes.filter(**kwargs).order_by(sort).all()
        )
    else:
        items = models.IdentityProvider.nodes.order_by(sort).all()
    if limit is None:
        return items[skip:]
    return items[skip : skip + limit]


def get_identity_provider(**kwargs) -> Optional[models.IdentityProvider]:
    return models.IdentityProvider.nodes.get_or_none(**kwargs)


def remove_identity_provider(item: models.IdentityProvider) -> bool:
    return item.delete()


def update_identity_provider(
    old_item: models.IdentityProvider, new_item: schemas.IdentityProviderUpdate
) -> Optional[models.IdentityProvider]:
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
