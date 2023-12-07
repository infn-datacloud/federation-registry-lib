from typing import Any, List, Optional, Union

# from app.user_group.api.dependencies import is_unique_user_group
# from app.user_group.crud import user_group
# from app.user_group.schemas import UserGroupCreate
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    Security,
    status,
)
from fastapi.security import HTTPBasicCredentials
from neomodel import db

from app.auth import flaat, security

# from app.auth_method.schemas import AuthMethodCreate
from app.identity_provider.api.dependencies import (
    valid_identity_provider_id,
    validate_new_identity_provider_values,
)
from app.identity_provider.crud import identity_provider_mng
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderQuery,
    IdentityProviderRead,
    IdentityProviderReadPublic,
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
        List[IdentityProviderReadExtendedPublic],
        List[IdentityProviderReadPublic],
    ],
    summary="Read all identity providers",
    description="Retrieve all identity providers stored in the database. \
        It is possible to filter on identity providers attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_identity_providers(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: IdentityProviderQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = identity_provider_mng.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = identity_provider_mng.paginate(items=items, page=page.page, size=page.size)
    return identity_provider_mng.choose_out_schema(
        items=items, auth=user_infos, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{identity_provider_uid}",
    response_model=Union[
        IdentityProviderReadExtended,
        IdentityProviderRead,
        IdentityProviderReadExtendedPublic,
        IdentityProviderReadPublic,
    ],
    summary="Read a specific identity provider",
    description="Retrieve a specific identity provider using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_identity_provider(
    size: SchemaSize = Depends(),
    item: IdentityProvider = Depends(valid_identity_provider_id),
    user_infos: Optional[Any] = None,
):
    return identity_provider_mng.choose_out_schema(
        items=[item], auth=user_infos, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{identity_provider_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[IdentityProviderRead],
    dependencies=[
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
@flaat.access_level("write")
def put_identity_provider(
    request: Request,
    update_data: IdentityProviderUpdate,
    response: Response,
    item: IdentityProvider = Depends(valid_identity_provider_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = identity_provider_mng.update(db_obj=item, obj_in=update_data)
    if not db_item:
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
@flaat.access_level("write")
def delete_identity_providers(
    request: Request,
    item: IdentityProvider = Depends(valid_identity_provider_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not identity_provider_mng.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


# @db.write_transaction
# @router.put(
#     "/{identity_provider_uid}/providers/{provider_uid}",
#     response_model=Optional[IdentityProviderReadExtended],
#
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
#
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
#     dependencies=[ Depends(is_unique_user_group)],
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
