from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/services", tags=["services"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Service)
def read_service(uid: UUID):
    db_item = crud.get_service(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Service])
def update_service(uid: UUID, item: schemas.ServiceUpdate):
    db_item = crud.get_service(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    return crud.update_service(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_services(uid: UUID):
    db_item = crud.get_service(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    if not crud.remove_service(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


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
