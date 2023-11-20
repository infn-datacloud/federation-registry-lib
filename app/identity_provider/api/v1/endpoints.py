from typing import List, Optional, Union

# from app.user_group.api.dependencies import is_unique_user_group
# from app.user_group.crud import user_group
# from app.user_group.schemas import UserGroupCreate
from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

from app.auth import check_read_access, check_write_access

# from app.auth_method.schemas import AuthMethodCreate
from app.identity_provider.api.dependencies import (
    valid_identity_provider_id,
    validate_new_identity_provider_values,
)
from app.identity_provider.crud import identity_provider
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderQuery,
    IdentityProviderRead,
    IdentityProviderReadPublic,
    IdentityProviderReadShort,
    IdentityProviderUpdate,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
)

# from app.project.schemas_extended import UserGroupReadExtended
# from app.provider.api.dependencies import valid_provider_id
# from app.provider.models import Provider
from app.query import DbQueryCommonParams, Pagination, SchemaSize

router = APIRouter(prefix="/identity_providers", tags=["identity_providers"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[IdentityProviderReadExtended],
        List[IdentityProviderRead],
        List[IdentityProviderReadShort],
        List[IdentityProviderReadExtendedPublic],
        List[IdentityProviderReadPublic],
    ],
    summary="Read all identity providers",
    description="Retrieve all identity providers stored in the database. \
        It is possible to filter on identity providers attributes and other \
        common query parameters.",
)
def get_identity_providers(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: IdentityProviderQuery = Depends(),
):
    items = identity_provider.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = identity_provider.paginate(items=items, page=page.page, size=page.size)
    return identity_provider.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{identity_provider_uid}",
    response_model=Union[
        IdentityProviderReadExtended,
        IdentityProviderRead,
        IdentityProviderReadShort,
        IdentityProviderReadExtendedPublic,
        IdentityProviderReadPublic,
    ],
    summary="Read a specific identity provider",
    description="Retrieve a specific identity provider using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_identity_provider(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: IdentityProvider = Depends(valid_identity_provider_id),
):
    return identity_provider.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{identity_provider_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[IdentityProviderRead],
    dependencies=[
        Depends(check_write_access),
        Depends(validate_new_identity_provider_values),
    ],
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
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{identity_provider_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
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


# @db.write_transaction
# @router.put(
#     "/{identity_provider_uid}/providers/{provider_uid}",
#     response_model=Optional[IdentityProviderReadExtended],
#     dependencies=[Depends(check_write_access)],
#     summary="Connect provider to identity provider",
#     description="Connect a provider to a specific identity \
#         provider knowing their *uid*s. \
#         If no entity matches the given *uid*s, the endpoint \
#         raises a `not found` error.",
# )
# def connect_provider_to_identity_providers(
#     data: AuthMethodCreate,
#     response: Response,
#     item: IdentityProvider = Depends(valid_identity_provider_id),
#     provider: Provider = Depends(valid_provider_id),
# ):
#     if item.providers.is_connected(provider):
#         db_item = item.providers.relationship(provider)
#         if all(
#             [
#                 db_item.__getattribute__(k) == v
#                 for k, v in data.dict(exclude_unset=True).items()
#             ]
#         ):
#             response.status_code = status.HTTP_304_NOT_MODIFIED
#             return None
#         item.providers.disconnect(provider)
#     item.providers.connect(provider, data.dict())
#     return item


# @db.write_transaction
# @router.delete(
#     "/{identity_provider_uid}/providers/{provider_uid}",
#     response_model=Optional[IdentityProviderReadExtended],
#     dependencies=[Depends(check_write_access)],
#     summary="Disconnect provider from identity provider",
#     description="Disconnect a provider from a specific identity \
#         provider knowing their *uid*s. \
#         If no entity matches the given *uid*s, the endpoint \
#         raises a `not found` error.",
# )
# def disconnect_provider_from_identity_providers(
#     response: Response,
#     item: IdentityProvider = Depends(valid_provider_id),
#     provider: Provider = Depends(valid_provider_id),
# ):
#     if not item.providers.is_connected(provider):
#         response.status_code = status.HTTP_304_NOT_MODIFIED
#         return None
#     item.providers.disconnect(provider)
#     return item


# @db.write_transaction
# @router.post(
#     "/{identity_provider_uid}/user_groups",
#     status_code=status.HTTP_201_CREATED,
#     response_model=UserGroupReadExtended,
#     dependencies=[Depends(check_write_access), Depends(is_unique_user_group)],
#     summary="Create a user group",
#     description="Create a user group belonging to identity provider \
#         identified by the given *uid*. \
#         If no entity matches the given *uid*, the endpoint \
#         raises a `not found` error. \
#         At first validate new user group values checking there are \
#         no other items, belonging to same identity provider, \
#         with the given *name*.",
# )
# def post_user_group(
#     item: UserGroupCreate,
#     db_item: IdentityProvider = Depends(valid_identity_provider_id),
# ):
#     return user_group.create(obj_in=item, identity_provider=db_item, force=True)
