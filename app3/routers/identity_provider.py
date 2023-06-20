from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_identity_provider_id
from .. import crud, schemas

router = APIRouter(prefix="/identity_providers", tags=["identity_providers"])

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


@db.read_transaction
@router.get("/{uid}", response_model=schemas.IdentityProvider)
def read_identity_provider(
    item: Mapping = Depends(valid_identity_provider_id),
):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.IdentityProvider])
def update_identity_provider(
    update_data: schemas.IdentityProviderUpdate,
    item: Mapping = Depends(valid_identity_provider_id),
):
    return crud.update_identity_provider(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_identity_providers(
    item: Mapping = Depends(valid_identity_provider_id),
):
    if not crud.remove_identity_provider(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


