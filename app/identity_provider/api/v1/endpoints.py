from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from app.identity_provider.api.dependencies import valid_identity_provider_id
from app.identity_provider.crud import identity_provider
from app.identity_provider.models import (
    IdentityProvider as IdentityProviderModel,
)
from app.identity_provider.schemas import (
    IdentityProviderQuery,
    IdentityProviderUpdate,
)
from app.identity_provider.schemas_extended import IdentityProviderReadExtended
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery
from app.user_group.schemas import UserGroupCreate
from app.user_group.api.dependencies import is_unique_user_group
from app.user_group.crud import user_group

router = APIRouter(prefix="/identity_providers", tags=["identity_providers"])


@db.read_transaction
@router.get("/", response_model=List[IdentityProviderReadExtended])
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
@router.get(
    "/{identity_provider_uid}", response_model=IdentityProviderReadExtended
)
def get_identity_provider(
    item: IdentityProviderModel = Depends(valid_identity_provider_id),
):
    return item


@db.write_transaction
@router.put(
    "/{identity_provider_uid}",
    response_model=Optional[IdentityProviderReadExtended],
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


@db.write_transaction
@router.post(
    "/{identity_provider_uid}/user_groups",
    status_code=status.HTTP_201_CREATED,
    response_model=IdentityProviderReadExtended,
)
def post_user_group(
    db_item: IdentityProviderModel = Depends(valid_identity_provider_id),
    item: UserGroupCreate = Depends(is_unique_user_group),
):
    db_obj = user_group.create(obj_in=item)
    db_item.user_groups.connect(db_obj)
    return db_item
