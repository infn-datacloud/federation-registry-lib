from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_quota_id
from .. import crud, schemas

router = APIRouter(prefix="/quotas", tags=["quotas"])


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


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Quota)
def read_quota(item: Mapping = Depends(valid_quota_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Quota])
def update_quota(
    update_data: schemas.QuotaUpdate,
    item: Mapping = Depends(valid_quota_id),
):
    return crud.update_quota(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotas(item: Mapping = Depends(valid_quota_id)):
    if not crud.remove_quota(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
