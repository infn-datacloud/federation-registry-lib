from typing import List, Optional
from .. import schemas, models


def create_identity_provider(
    item: schemas.IdentityProviderCreate,
) -> schemas.IdentityProvider:
    return models.IdentityProvider(**item.dict()).save()


def get_identity_providers(**kwargs) -> List[schemas.IdentityProvider]:
    if kwargs:
        return models.IdentityProvider.nodes.filter(**kwargs).all()
    return models.IdentityProvider.nodes.all()


def get_identity_provider(**kwargs) -> Optional[schemas.IdentityProvider]:
    return models.IdentityProvider.nodes.get_or_none(**kwargs)


def remove_identity_provider(item: models.IdentityProvider) -> bool:
    return item.delete()
