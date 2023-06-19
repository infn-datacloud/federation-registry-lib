from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/quotas", tags=["quotas"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Quota)
def read_quota(uid: UUID):
    db_item = crud.get_quota(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quota not found",
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Quota])
def update_quota(uid: UUID, item: schemas.QuotaUpdate):
    db_item = crud.get_quota(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quota not found",
        )
    return crud.update_quota(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotas(uid: UUID):
    db_item = crud.get_quota(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quota not found",
        )
    if not crud.remove_quota(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.Quota])
def read_quotas(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.QuotaBase = Depends(),
):
    items = crud.get_quotas(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )

    return paginate(items=items, page=page.page, size=page.size)
