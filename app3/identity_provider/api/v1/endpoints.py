from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_identity_provider_id
from ...crud import identity_provider
from ...models import IdentityProvider as IdentityProviderModel
from ...schemas import (
    IdentityProvider,
    IdentityProviderQuery,
    IdentityProviderUpdate,
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
@router.put(
    "/{identity_provider_uid}", response_model=Optional[IdentityProvider]
)
def put_identity_provider(
    update_data: IdentityProviderUpdate,
    item: IdentityProviderModel = Depends(valid_identity_provider_id),
):
    return identity_provider.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete(
    "/{identity_provider_uid}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_identity_providers(
    item: IdentityProviderModel = Depends(valid_identity_provider_id),
):
    if not identity_provider.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
