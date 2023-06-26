from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from .crud import edit_quota_type, read_quota_types, remove_quota_type
from .dependencies import valid_quota_type_id
from .models import QuotaType as QuotaTypeModel
from .schemas import QuotaType, QuotaTypePatch, QuotaTypeQuery
from ..pagination import Pagination, paginate
from ..query import CommonGetQuery

router = APIRouter(prefix="/quota_types", tags=["quota_types"])


@db.read_transaction
@router.get("/", response_model=List[QuotaType])
def get_quota_types(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: QuotaTypeQuery = Depends(),
):
    items = read_quota_types(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{quota_type_uid}", response_model=QuotaType)
def get_quota_type(item: QuotaTypeModel = Depends(valid_quota_type_id)):
    return item


@db.write_transaction
@router.patch("/{quota_type_uid}", response_model=Optional[QuotaType])
def patch_quota_type(
    update_data: QuotaTypePatch,
    item: QuotaTypeModel = Depends(valid_quota_type_id),
):
    return edit_quota_type(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{quota_type_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quota_types(item: QuotaTypeModel = Depends(valid_quota_type_id)):
    if not remove_quota_type(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
