from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_service_type_id
from .. import crud, schemas

router = APIRouter(prefix="/service_types", tags=["service_types"])


@db.read_transaction
@router.get("/", response_model=List[schemas.ServiceType])
def read_service_types(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.ServiceTypeBase = Depends(),
):
    items = crud.get_service_types(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.ServiceType)
def read_service_type(item: Mapping = Depends(valid_service_type_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.ServiceType])
def update_service_type(
    update_data: schemas.ServiceTypeUpdate,
    item: Mapping = Depends(valid_service_type_id),
):
    return crud.update_service_type(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_types(item: Mapping = Depends(valid_service_type_id)):
    if not crud.remove_service_type(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
