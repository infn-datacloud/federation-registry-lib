from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .crud import (
    create_service_type,
    edit_service_type,
    read_service_types,
    remove_service_type,
)
from .dependenecies import valid_service_type_id, is_unique_service_type
from .schemas import (
    ServiceType,
    ServiceTypeCreate,
    ServiceTypePatch,
    ServiceTypeQuery,
)
from ..pagination import Pagination, paginate
from ..query import CommonGetQuery

router = APIRouter(prefix="/service_types", tags=["service_types"])


@db.write_transaction
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ServiceType
)
def post_service_type(
    item: ServiceTypeCreate = Depends(is_unique_service_type),
):
    return create_service_type(item)


@db.read_transaction
@router.get("/", response_model=List[ServiceType])
def get_service_types(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ServiceTypeQuery = Depends(),
):
    items = read_service_types(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{service_type_uid}", response_model=ServiceType)
def get_service_type(item: Mapping = Depends(valid_service_type_id)):
    return item


@db.write_transaction
@router.patch("/{service_type_uid}", response_model=Optional[ServiceType])
def patch_service_type(
    update_data: ServiceTypePatch,
    item: Mapping = Depends(valid_service_type_id),
):
    return edit_service_type(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{service_type_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_types(item: Mapping = Depends(valid_service_type_id)):
    if not remove_service_type(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
