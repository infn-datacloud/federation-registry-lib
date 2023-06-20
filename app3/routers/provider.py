from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_provider_id
from .. import crud, schemas

router = APIRouter(prefix="/providers", tags=["providers"])


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
def read_provider(item: Mapping = Depends(valid_provider_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=schemas.Provider)
def update_provider(
    update_data: schemas.ProviderUpdate,
    item: Mapping = Depends(valid_provider_id),
):
    return crud.update_provider(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_providers(item: Mapping = Depends(valid_provider_id)):
    if not crud.remove_provider(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
