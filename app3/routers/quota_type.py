from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_quota_type_id
from .. import crud, schemas

router = APIRouter(prefix="/quota_types", tags=["quota_types"])


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


@db.read_transaction
@router.get("/{uid}", response_model=schemas.QuotaType)
def read_quota_type(item: Mapping = Depends(valid_quota_type_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.QuotaType])
def update_quota_type(
    update_data: schemas.QuotaTypeUpdate,
    item: Mapping = Depends(valid_quota_type_id),
):
    return crud.update_quota_type(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quota_types(item: Mapping = Depends(valid_quota_type_id)):
    if not crud.remove_quota_type(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
