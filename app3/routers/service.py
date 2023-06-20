from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_service_id
from .. import crud, schemas

router = APIRouter(prefix="/services", tags=["services"])


@db.read_transaction
@router.get("/", response_model=List[schemas.Service])
def read_services(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.ServiceBase = Depends(),
):
    items = crud.get_services(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Service)
def read_service(item: Mapping = Depends(valid_service_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Service])
def update_service(
    update_data: schemas.ServiceUpdate,
    item: Mapping = Depends(valid_service_id),
):
    return crud.update_service(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_services(item: Mapping = Depends(valid_service_id)):
    if not crud.remove_service(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
