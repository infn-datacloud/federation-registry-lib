from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_cluster_id
from .. import crud, schemas

router = APIRouter(prefix="/clusters", tags=["clusters"])


@db.read_transaction
@router.get("/", response_model=List[schemas.Cluster])
def read_clusters(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.ClusterBase = Depends(),
):
    items = crud.get_clusters(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Cluster)
def read_cluster(item: Mapping = Depends(valid_cluster_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Cluster])
def update_cluster(
    update_data: schemas.ClusterUpdate,
    item: Mapping = Depends(valid_cluster_id),
):
    return crud.update_cluster(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clusters(item: Mapping = Depends(valid_cluster_id)):
    if not crud.remove_cluster(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
