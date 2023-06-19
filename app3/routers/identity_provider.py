from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/identity_providers", tags=["identity_providers"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.IdentityProvider)
def read_identity_provider(uid: UUID):
    db_item = crud.get_identity_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IdentityProvider not found",
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.IdentityProvider])
def update_identity_provider(uid: UUID, item: schemas.IdentityProviderUpdate):
    db_item = crud.get_identity_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IdentityProvider not found",
        )
    return crud.update_identity_provider(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_identity_providers(uid: UUID):
    db_item = crud.get_identity_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IdentityProvider not found",
        )
    if not crud.remove_identity_provider(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.IdentityProvider])
def read_identity_providers(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.IdentityProviderBase = Depends(),
):
    items = crud.get_identity_providers(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )

    return paginate(items=items, page=page.page, size=page.size)
