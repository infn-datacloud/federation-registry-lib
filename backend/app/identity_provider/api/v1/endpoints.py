from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db
from typing import List, Optional

from app.identity_provider.api.dependencies import (
    valid_identity_provider_endpoint,
    validate_new_identity_provider_values,
    valid_identity_provider_id,
)
from app.identity_provider.crud import identity_provider
from app.identity_provider.models import (
    IdentityProvider,
)
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderQuery,
    IdentityProviderUpdate,
)
from app.identity_provider.schemas_extended import IdentityProviderReadExtended
from app.pagination import Pagination, paginate
from app.project.schemas_extended import UserGroupReadExtended
from app.query import CommonGetQuery
from app.user_group.schemas import UserGroupCreate
from app.user_group.api.dependencies import is_unique_user_group
from app.user_group.crud import user_group

router = APIRouter(prefix="/identity_providers", tags=["identity_providers"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[IdentityProviderReadExtended],
    summary="Read all identity providers",
    description="Retrieve all identity providers stored in the database. \
        It is possible to filter on identity providers attributes and other \
        common query parameters.",
)
def get_identity_providers(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: IdentityProviderQuery = Depends(),
):
    items = identity_provider.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IdentityProviderReadExtended,
    dependencies=[Depends(valid_identity_provider_endpoint)],
    summary="Create location",
    description="Create a location. \
        At first validate new location values checking there are \
        no other items with the given *name*.",
)
def post_location(item: IdentityProviderCreate):
    return identity_provider.create(obj_in=item, force=True)


@db.read_transaction
@router.get(
    "/{identity_provider_uid}",
    response_model=IdentityProviderReadExtended,
    summary="Read a specific identity provider",
    description="Retrieve a specific identity provider using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_identity_provider(
    item: IdentityProvider = Depends(valid_identity_provider_id),
):
    return item


@db.write_transaction
@router.patch(
    "/{identity_provider_uid}",
    response_model=Optional[IdentityProviderReadExtended],
    dependencies=[Depends(validate_new_identity_provider_values)],
    summary="Edit a specific identity provider",
    description="Update attribute values of a specific identity provider. \
        The target identity provider is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new identity provider values checking there are \
        no other items with the given *endpoint*.",
)
def put_identity_provider(
    update_data: IdentityProviderUpdate,
    response: Response,
    item: IdentityProvider = Depends(valid_identity_provider_id),
):
    db_item = identity_provider.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{identity_provider_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific identity provider",
    description="Delete a specific identity provider using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related user groups.",
)
def delete_identity_providers(
    item: IdentityProvider = Depends(valid_identity_provider_id),
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
    response_model=UserGroupReadExtended,
    dependencies=[Depends(is_unique_user_group)],
    summary="Create a user group",
    description="Create a user group belonging to identity provider \
        identified by the given *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        At first validate new user group values checking there are \
        no other items, belonging to same identity provider, \
        with the given *name*.",
)
def post_user_group(
    item: UserGroupCreate,
    db_item: IdentityProvider = Depends(valid_identity_provider_id),
):
    return user_group.create(
        obj_in=item, identity_provider=db_item, force=True
    )
