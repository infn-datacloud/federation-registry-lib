from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_identity_provider_id
from ...crud import identity_provider
from ...models import IdentityProvider as IdentityProviderModel
from ...schemas import (
    IdentityProvider,
    IdentityProviderPatch,
    IdentityProviderQuery,
)
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/identity_providers", tags=["identity_providers"])


@db.read_transaction
@router.get("/", response_model=List[IdentityProvider])
def get_identity_providers(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: IdentityProviderQuery = Depends(),
):
    items = identity_provider.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{identity_provider_uid}", response_model=IdentityProvider)
def get_identity_provider(
    item: IdentityProviderModel = Depends(valid_identity_provider_id),
):
    return item


@db.write_transaction
@router.patch(
    "/{identity_provider_uid}", response_model=Optional[IdentityProvider]
)
def patch_identity_provider(
    update_data: IdentityProviderPatch,
    item: IdentityProviderModel = Depends(valid_identity_provider_id),
):
    return identity_provider.update(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete(
    "/{identity_provider_uid}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_identity_providers(
    item: IdentityProviderModel = Depends(valid_identity_provider_id),
):
    if not identity_provider.remove(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
