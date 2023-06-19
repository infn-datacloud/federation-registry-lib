from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/quota_types", tags=["quota_types"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.QuotaType)
def read_quota_type(uid: UUID):
    db_item = crud.get_quota_type(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QuotaType not found",
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.QuotaType])
def update_quota_type(uid: UUID, item: schemas.QuotaTypeUpdate):
    db_item = crud.get_quota_type(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QuotaType not found",
        )
    return crud.update_quota_type(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quota_types(uid: UUID):
    db_item = crud.get_quota_type(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QuotaType not found",
        )
    if not crud.remove_quota_type(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.QuotaType])
def read_quota_types(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.QuotaTypeBase = Depends(),
):
    items = crud.get_quota_types(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )

    return paginate(items=items, page=page.page, size=page.size)
