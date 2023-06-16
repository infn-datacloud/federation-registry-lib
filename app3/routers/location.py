from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/locations", tags=["locations"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Location)
def read_locations(uid: UUID):
    db_item = crud.get_location(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Location])
def update_location(uid: UUID, item: schemas.LocationUpdate):
    db_item = crud.get_location(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )
    return crud.update_location(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(uid: UUID):
    db_item = crud.get_location(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )
    if not crud.remove_location(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.Location])
def read_locations(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.LocationBase = Depends(),
):
    items = crud.get_locations(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)
