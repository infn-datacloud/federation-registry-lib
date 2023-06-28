from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_quota_id
from ...crud import quota
from ...models import Quota as QuotaModel
from ...schemas import QuotaQuery, QuotaUpdate
from ...schemas_extended import QuotaExtended
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/quotas", tags=["quotas"])


@db.read_transaction
@router.get("/", response_model=List[QuotaExtended])
def get_quotas(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: QuotaQuery = Depends(),
):
    items = quota.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{quota_uid}", response_model=QuotaExtended)
def get_quota(item: QuotaModel = Depends(valid_quota_id)):
    return item


@db.write_transaction
@router.put("/{quota_uid}", response_model=Optional[QuotaExtended])
def put_quota(
    update_data: QuotaUpdate,
    item: QuotaModel = Depends(valid_quota_id),
):
    return quota.update(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{quota_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotas(item: QuotaModel = Depends(valid_quota_id)):
    if not quota.remove(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
