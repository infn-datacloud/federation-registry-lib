from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_quota_type_id
from ...crud import quota_type
from ...models import QuotaType as QuotaTypeModel
from ...schemas import QuotaType, QuotaTypeQuery, QuotaTypeUpdate
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/quota_types", tags=["quota_types"])


@db.read_transaction
@router.get("/", response_model=List[QuotaType])
def get_quota_types(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: QuotaTypeQuery = Depends(),
):
    items = quota_type.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{quota_type_uid}", response_model=QuotaType)
def get_quota_type(item: QuotaTypeModel = Depends(valid_quota_type_id)):
    return item


@db.write_transaction
@router.put("/{quota_type_uid}", response_model=Optional[QuotaType])
def put_quota_type(
    update_data: QuotaTypeUpdate,
    item: QuotaTypeModel = Depends(valid_quota_type_id),
):
    return quota_type.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{quota_type_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quota_types(item: QuotaTypeModel = Depends(valid_quota_type_id)):
    if not quota_type.remove(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
