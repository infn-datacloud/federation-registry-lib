from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_cluster_id
from ...crud import cluster
from ...models import Cluster as ClusterModel
from ...schemas import Cluster, ClusterQuery, ClusterUpdate
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/clusters", tags=["clusters"])


@db.read_transaction
@router.get("/", response_model=List[Cluster])
def get_clusters(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ClusterQuery = Depends(),
):
    items = cluster.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{cluster_uid}", response_model=Cluster)
def get_cluster(item: ClusterModel = Depends(valid_cluster_id)):
    return item


@db.write_transaction
@router.put("/{cluster_uid}", response_model=Optional[Cluster])
def put_cluster(
    update_data: ClusterUpdate,
    item: ClusterModel = Depends(valid_cluster_id),
):
    return cluster.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{cluster_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clusters(item: ClusterModel = Depends(valid_cluster_id)):
    if not cluster.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
