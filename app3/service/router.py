from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .crud import edit_service, read_services, remove_service
from .dependencies import valid_service_id
from .schemas import Service, ServicePatch, ServiceQuery
from ..pagination import Pagination, paginate
from ..query import CommonGetQuery

router = APIRouter(prefix="/services", tags=["services"])


@db.read_transaction
@router.get("/", response_model=List[Service])
def get_services(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ServiceQuery = Depends(),
):
    items = read_services(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{service_uid}", response_model=Service)
def get_service(item: Mapping = Depends(valid_service_id)):
    return item


@db.write_transaction
@router.patch("/{service_uid}", response_model=Optional[Service])
def patch_service(
    update_data: ServicePatch,
    item: Mapping = Depends(valid_service_id),
):
    return edit_service(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{service_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_services(item: Mapping = Depends(valid_service_id)):
    if not remove_service(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
