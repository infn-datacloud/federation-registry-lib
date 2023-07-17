from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from app.quota.api.dependencies import valid_quota_id
from app.quota.crud import quota
from app.quota.models import Quota as QuotaModel
from app.quota.schemas import QuotaQuery, QuotaUpdate
from app.quota.schemas_extended import QuotaReadExtended
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery

router = APIRouter(prefix="/quotas", tags=["quotas"])


@db.read_transaction
@router.get("/", response_model=List[QuotaReadExtended])
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
@router.get("/{quota_uid}", response_model=QuotaReadExtended)
def get_quota(item: QuotaModel = Depends(valid_quota_id)):
    return item


@db.write_transaction
@router.put("/{quota_uid}", response_model=Optional[QuotaReadExtended])
def put_quota(
    update_data: QuotaUpdate,
    item: QuotaModel = Depends(valid_quota_id),
):
    return quota.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{quota_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotas(item: QuotaModel = Depends(valid_quota_id)):
    if not quota.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
