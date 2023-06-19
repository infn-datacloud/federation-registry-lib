from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/providers", tags=["providers"])


@db.write_transaction
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Provider
)
def add_provider(item: schemas.ProviderCreate):
    db_item = crud.get_provider(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider already registered",
        )
    return crud.create_provider(item)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Provider)
def read_provider(uid: UUID):
    db_item = crud.get_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=schemas.Provider)
def update_provider(uid: UUID, item: schemas.ProviderUpdate):
    db_item = crud.get_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found"
        )
    return crud.update_provider(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_providers(uid: UUID):
    db_item = crud.get_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found"
        )
    if not crud.remove_provider(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.Provider])
def read_providers(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.UserGroupBase = Depends(),
):
    items = crud.get_providers(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)
