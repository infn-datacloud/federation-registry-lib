from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/flavors", tags=["flavors"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Flavor)
def read_flavor(uid: UUID):
    db_item = crud.get_flavor(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flavor not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Flavor])
def update_flavor(uid: UUID, item: schemas.FlavorUpdate):
    db_item = crud.get_flavor(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flavor not found"
        )
    return crud.update_flavor(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flavors(uid: UUID):
    db_item = crud.get_flavor(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flavor not found"
        )
    if not crud.remove_flavor(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.Flavor])
def read_flavors(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.FlavorBase = Depends(),
):
    items = crud.get_flavors(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )

    return paginate(items=items, page=page.page, size=page.size)
