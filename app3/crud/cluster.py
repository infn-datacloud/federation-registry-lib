from typing import List, Optional

from .utils import truncate, update
from .. import schemas, models


def create_cluster(item: schemas.ClusterCreate) -> models.Cluster:
    return models.Cluster.get_or_create(item.dict())[0]


def read_clusters(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Cluster]:
    if kwargs:
        items = models.Cluster.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Cluster.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_cluster(**kwargs) -> Optional[models.Cluster]:
    return models.Cluster.nodes.get_or_none(**kwargs)


def remove_cluster(item: models.Cluster) -> bool:
    return item.delete()


def edit_cluster(
    old_item: models.Cluster, new_item: schemas.ClusterPatch
) -> Optional[models.Cluster]:
    return update(old_item=old_item, new_item=new_item)
