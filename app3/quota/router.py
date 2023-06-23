from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .crud import edit_quota, read_quotas, remove_quota
from .dependencies import valid_quota_id
from .schemas import Quota, QuotaPatch, QuotaQuery
from ..pagination import Pagination, paginate
from ..query import CommonGetQuery

router = APIRouter(prefix="/quotas", tags=["quotas"])


@db.read_transaction
@router.get("/", response_model=List[Quota])
def get_quotas(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: QuotaQuery = Depends(),
):
    items = read_quotas(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{quota_uid}", response_model=Quota)
def get_quota(item: Mapping = Depends(valid_quota_id)):
    return item


@db.write_transaction
@router.patch("/{quota_uid}", response_model=Optional[Quota])
def patch_quota(
    update_data: QuotaPatch,
    item: Mapping = Depends(valid_quota_id),
):
    return edit_quota(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{quota_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotas(item: Mapping = Depends(valid_quota_id)):
    if not remove_quota(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
