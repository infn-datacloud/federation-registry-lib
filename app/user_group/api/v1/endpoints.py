from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBasicCredentials
from neomodel import db

from app.auth.dependencies import (
    check_read_access,
    flaat,
    lazy_security,
    strict_security,
)
from app.provider.enum import ProviderType
from app.provider.schemas import ProviderQuery

# from app.flavor.crud import flavor
# from app.flavor.schemas import FlavorRead, FlavorReadPublic, FlavorReadShort
# from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
# from app.identity_provider.schemas_extended import (
#     ProviderReadExtended,
#     ProviderReadExtendedPublic,
# )
# from app.image.crud import image
# from app.image.schemas import ImageRead, ImageReadPublic, ImageReadShort
# from app.image.schemas_extended import ImageReadExtended, ImageReadExtendedPublic
# from app.provider.crud import provider
# from app.provider.schemas import ProviderRead, ProviderReadPublic, ProviderReadShort
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.region.schemas import RegionQuery

# from app.service.schemas import (
#     BlockStorageServiceRead,
#     BlockStorageServiceReadPublic,
#     BlockStorageServiceReadShort,
#     ComputeServiceRead,
#     ComputeServiceReadPublic,
#     ComputeServiceReadShort,
#     IdentityServiceRead,
#     IdentityServiceReadPublic,
#     IdentityServiceReadShort,
# )
# from app.service.schemas_extended import (
#     BlockStorageServiceReadExtended,
#     BlockStorageServiceReadExtendedPublic,
#     ComputeServiceReadExtended,
#     ComputeServiceReadExtendedPublic,
#     IdentityServiceReadExtended,
#     IdentityServiceReadExtendedPublic,
# )
from app.user_group.api.dependencies import (
    valid_user_group_id,
    validate_new_user_group_values,
)
from app.user_group.api.utils import filter_on_provider_attr, filter_on_region_attr
from app.user_group.crud import user_group
from app.user_group.models import UserGroup
from app.user_group.schemas import (
    UserGroupQuery,
    UserGroupRead,
    UserGroupReadPublic,
    UserGroupReadShort,
    UserGroupUpdate,
)
from app.user_group.schemas_extended import (
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)

router = APIRouter(prefix="/user_groups", tags=["user_groups"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[UserGroupReadExtended],
        List[UserGroupRead],
        List[UserGroupReadShort],
        List[UserGroupReadExtendedPublic],
        List[UserGroupReadPublic],
    ],
    summary="Read all user groups",
    description="Retrieve all user groups stored in the database. \
        It is possible to filter on user groups attributes and other \
        common query parameters.",
)
@check_read_access
def get_user_groups(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: UserGroupQuery = Depends(),
    idp_endpoint: Optional[str] = None,
    provider_name: Optional[str] = None,
    provider_type: Optional[ProviderType] = None,
    region_name: Optional[str] = None,
    client_credentials: HTTPBasicCredentials = Depends(lazy_security),
    auth: bool = False,
):
    items = user_group.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    if idp_endpoint:
        items = filter(
            lambda x: x.identity_provider.single().endpoint == idp_endpoint, items
        )

    if provider_type:
        provider_type = provider_type.value
    provider_query = ProviderQuery(name=provider_name, type=provider_type)
    items = filter_on_provider_attr(items=items, provider_query=provider_query)

    region_query = RegionQuery(name=region_name)
    items = filter_on_region_attr(items=items, region_query=region_query)

    items = user_group.paginate(items=items, page=page.page, size=page.size)
    return user_group.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{user_group_uid}",
    response_model=Union[
        UserGroupReadExtended,
        UserGroupRead,
        UserGroupReadShort,
        UserGroupReadExtendedPublic,
        UserGroupReadPublic,
    ],
    summary="Read a specific user group",
    description="Retrieve a specific user group using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@check_read_access
def get_user_group(
    size: SchemaSize = Depends(),
    item: UserGroup = Depends(valid_user_group_id),
    client_credentials: HTTPBasicCredentials = Depends(lazy_security),
    auth: bool = False,
):
    return user_group.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{user_group_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[UserGroupRead],
    dependencies=[Depends(validate_new_user_group_values)],
    summary="Edit a specific user group",
    description="Update attribute values of a specific user group. \
        The target user group is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new user group values checking there are \
        no other items, belonging to same identity provider, \
        with the given *name*.",
)
@flaat.access_level("write")
def put_user_group(
    request: Request,
    update_data: UserGroupUpdate,
    response: Response,
    item: UserGroup = Depends(valid_user_group_id),
    client_credentials: HTTPBasicCredentials = Depends(strict_security),
):
    db_item = user_group.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{user_group_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific user group",
    description="Delete a specific user group using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related SLAs.",
)
@flaat.access_level("write")
def delete_user_group(
    request: Request,
    item: UserGroup = Depends(valid_user_group_id),
    client_credentials: HTTPBasicCredentials = Depends(strict_security),
):
    if not user_group.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


# @db.read_transaction
# @router.get(
#     "/{user_group_uid}/flavors",
#     response_model=Union[
#         List[FlavorReadExtended],
#         List[FlavorRead],
#         List[FlavorReadShort],
#         List[FlavorReadExtendedPublic],
#         List[FlavorReadPublic],
#     ],
#     summary="Read user group accessible flavors",
#     description="Retrieve all the flavors the user group \
#         has access to thanks to its SLA. \
#         If no entity matches the given *uid*, the endpoint \
#         raises a `not found` error.",
# )
# def get_user_group_flavors(
#     auth: bool = Depends(check_read_access),
#     size: SchemaSize = Depends(),
#     item: UserGroup = Depends(valid_user_group_id),
# ):
#     return flavor.choose_out_schema(
#         items=item.flavors(), auth=auth, short=size.short, with_conn=size.with_conn
#     )


# @db.read_transaction
# @router.get(
#     "/{user_group_uid}/images",
#     response_model=Union[
#         List[ImageReadExtended],
#         List[ImageRead],
#         List[ImageReadShort],
#         List[ImageReadExtendedPublic],
#         List[ImageReadPublic],
#     ],
#     summary="Read user group accessible images",
#     description="Retrieve all the images the user group \
#         has access to thanks to its SLA. \
#         If no entity matches the given *uid*, the endpoint \
#         raises a `not found` error.",
# )
# def get_user_group_images(
#     auth: bool = Depends(check_read_access),
#     size: SchemaSize = Depends(),
#     item: UserGroup = Depends(valid_user_group_id),
# ):
#     return image.choose_out_schema(
#         items=item.images(), auth=auth, short=size.short, with_conn=size.with_conn
#     )


# @db.read_transaction
# @router.get(
#     "/{user_group_uid}/providers",
#     response_model=Union[
#         List[ProviderReadExtended],
#         List[ProviderRead],
#         List[ProviderReadShort],
#         List[ProviderReadExtendedPublic],
#         List[ProviderReadPublic],
#     ],
#     summary="Read user group accessible providers",
#     description="Retrieve all the providers the user group \
#         has access to thanks to its SLA. \
#         If no entity matches the given *uid*, the endpoint \
#         raises a `not found` error.",
# )
# def get_user_group_providers(
#     auth: bool = Depends(check_read_access),
#     size: SchemaSize = Depends(),
#     item: UserGroup = Depends(valid_user_group_id),
# ):
#     return provider.choose_out_schema(
#         items=item.providers(), auth=auth, short=size.short, with_conn=size.with_conn
#     )


# @db.read_transaction
# @router.get(
#    "/{user_group_uid}/services",
#    response_model=Union[
#        List[
#            Union[
#                BlockStorageServiceReadExtended,
#                IdentityServiceReadExtended,
#                ComputeServiceReadExtended,
#            ]
#        ],
#        List[Union[BlockStorageServiceRead, IdentityServiceRead, ComputeServiceRead]],
#        List[
#            Union[
#                BlockStorageServiceReadShort,
#                IdentityServiceReadShort,
#                ComputeServiceReadShort,
#            ]
#        ],
#        List[
#            Union[
#                BlockStorageServiceReadExtendedPublic,
#                IdentityServiceReadExtendedPublic,
#                ComputeServiceReadExtendedPublic,
#            ]
#        ],
#        List[
#            Union[
#                BlockStorageServiceReadPublic,
#                IdentityServiceReadPublic,
#                ComputeServiceReadPublic,
#            ]
#        ],
#    ],
#    summary="Read user group accessible services",
#    description="Retrieve all the services the user group \
#        has access to thanks to its SLA. \
#        If no entity matches the given *uid*, the endpoint \
#        raises a `not found` error.",
# )
# def get_user_group_services(
#    auth: bool = Depends(check_read_access),
#    size: SchemaSize = Depends(),
#    item: UserGroup = Depends(valid_user_group_id),
#    srv: ServiceQuery = Depends(),
# ):
#    items = item.services(**srv.dict(exclude_none=True))
#    return service.choose_out_schema(
#        items=items, auth=auth, short=size.short, with_conn=size.with_conn
#    )
