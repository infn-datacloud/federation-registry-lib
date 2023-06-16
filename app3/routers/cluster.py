from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/clusters", tags=["clusters"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Cluster)
def read_cluster(uid: UUID):
    db_item = crud.get_cluster(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Cluster])
def update_cluster(uid: UUID, item: schemas.ClusterUpdate):
    db_item = crud.get_cluster(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found"
        )
    return crud.update_cluster(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clusters(uid: UUID):
    db_item = crud.get_cluster(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found"
        )
    if not crud.remove_cluster(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


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
