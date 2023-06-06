from neomodel import db
from typing import List, Optional
from .. import schemas, models


@db.write_transaction
def create_provider(item: schemas.ProviderCreate) -> schemas.Provider:
    return models.Provider(**item.dict()).save()


@db.read_transaction
def get_providers(**kwargs) -> List[schemas.Provider]:
    if kwargs:
        return models.Provider.nodes.filter(**kwargs).all()
    return models.Provider.nodes.all()


@db.read_transaction
def get_provider(**kwargs) -> Optional[schemas.Provider]:
    return models.Provider.nodes.get_or_none(**kwargs)


def remove_provider(item: schemas.Provider) -> bool:
    return item.delete()
