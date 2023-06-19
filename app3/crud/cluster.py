from typing import List, Optional

from .utils import truncate
from .. import schemas, models


def create_cluster(item: schemas.ClusterCreate) -> models.Cluster:
    return models.Cluster(**item.dict()).save()


def get_clusters(
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


def get_cluster(**kwargs) -> Optional[models.Cluster]:
    return models.Cluster.nodes.get_or_none(**kwargs)


def remove_cluster(item: models.Cluster) -> bool:
    return item.delete()


def update_cluster(
    old_item: models.Cluster, new_item: schemas.ClusterUpdate
) -> Optional[models.Cluster]:
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
