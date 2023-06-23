from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .crud import edit_cluster, read_clusters, remove_cluster
from .dependencies import valid_cluster_id
from .schemas import Cluster, ClusterPatch, ClusterQuery
from ..pagination import Pagination, paginate
from ..query import CommonGetQuery

router = APIRouter(prefix="/clusters", tags=["clusters"])


@db.read_transaction
@router.get("/", response_model=List[Cluster])
def get_clusters(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ClusterQuery = Depends(),
):
    items = read_clusters(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{cluster_uid}", response_model=Cluster)
def get_cluster(item: Mapping = Depends(valid_cluster_id)):
    return item


@db.write_transaction
@router.patch("/{cluster_uid}", response_model=Optional[Cluster])
def patch_cluster(
    update_data: ClusterPatch,
    item: Mapping = Depends(valid_cluster_id),
):
    return edit_cluster(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{cluster_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clusters(item: Mapping = Depends(valid_cluster_id)):
    if not remove_cluster(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
