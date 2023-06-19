from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/service_types", tags=["service_types"])


@db.write_transaction
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ServiceType
)
def add_service_type(item: schemas.ServiceTypeCreate):
    db_item = crud.get_service_type(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ServiceType already registered",
        )
    return crud.create_service_type(item)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.ServiceType)
def read_service_type(uid: UUID):
    db_item = crud.get_service_type(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ServiceType not found",
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.ServiceType])
def update_service_type(uid: UUID, item: schemas.ServiceTypeUpdate):
    db_item = crud.get_service_type(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ServiceType not found",
        )
    return crud.update_service_type(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_types(uid: UUID):
    db_item = crud.get_service_type(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ServiceType not found",
        )
    if not crud.remove_service_type(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


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
