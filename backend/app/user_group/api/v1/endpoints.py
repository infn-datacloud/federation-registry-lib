from typing import List, Optional, Union

from app.auth.dependencies import check_read_access, check_write_access
from app.flavor.crud import flavor
from app.flavor.schemas import FlavorRead
from app.image.crud import image
from app.image.schemas import ImageRead
from app.provider.crud import provider
from app.provider.schemas import ProviderRead
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.service.crud import service
from app.service.schemas_extended import (
    ChronosServiceReadExtended,
    KubernetesServiceReadExtended,
    MarathonServiceReadExtended,
    MesosServiceReadExtended,
    NovaServiceReadExtended,
    OneDataServiceReadExtended,
    RucioServiceReadExtended,
)
from app.user_group.api.dependencies import (
    valid_user_group_id,
    validate_new_user_group_values,
)
from app.user_group.crud import user_group
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupQuery, UserGroupUpdate
from app.user_group.schemas_extended import ServiceQuery, UserGroupReadExtended
from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

router = APIRouter(prefix="/user_groups", tags=["user_groups"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[UserGroupReadExtended],
    summary="Read all user groups",
    description="Retrieve all user groups stored in the database. \
        It is possible to filter on user groups attributes and other \
        common query parameters.",
)
def get_user_groups(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: UserGroupQuery = Depends(),
):
    items = user_group.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = user_group.paginate(items=items, page=page.page, size=page.size)
    return user_group.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{user_group_uid}",
    response_model=UserGroupReadExtended,
    summary="Read a specific user group",
    description="Retrieve a specific user group using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_user_group(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: UserGroup = Depends(valid_user_group_id),
):
    return user_group.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{user_group_uid}",
    response_model=Optional[UserGroupReadExtended],
    dependencies=[Depends(check_write_access), Depends(validate_new_user_group_values)],
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
def put_user_group(
    update_data: UserGroupUpdate,
    response: Response,
    item: UserGroup = Depends(valid_user_group_id),
):
    db_item = user_group.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{user_group_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific user group",
    description="Delete a specific user group using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related SLAs.",
)
def delete_user_group(item: UserGroup = Depends(valid_user_group_id)):
    if not user_group.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get(
    "/{user_group_uid}/flavors",
    response_model=List[FlavorRead],
    summary="Read user group accessible flavors",
    description="Retrieve all the flavors the user group \
        has access to thanks to its SLA. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_user_group_flavors(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: UserGroup = Depends(valid_user_group_id),
):
    return flavor.choose_out_schema(
        items=item.flavors(), auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{user_group_uid}/images",
    response_model=List[ImageRead],
    summary="Read user group accessible images",
    description="Retrieve all the images the user group \
        has access to thanks to its SLA. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_user_group_images(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: UserGroup = Depends(valid_user_group_id),
):
    return image.choose_out_schema(
        items=item.images(), auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{user_group_uid}/providers",
    response_model=List[ProviderRead],
    summary="Read user group accessible providers",
    description="Retrieve all the providers the user group \
        has access to thanks to its SLA. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_user_group_providers(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: UserGroup = Depends(valid_user_group_id),
):
    return provider.choose_out_schema(
        items=item.providers(), auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@router.get(
    "/{user_group_uid}/services",
    response_model=List[
        Union[
            ChronosServiceReadExtended,
            KubernetesServiceReadExtended,
            MarathonServiceReadExtended,
            MesosServiceReadExtended,
            NovaServiceReadExtended,
            OneDataServiceReadExtended,
            RucioServiceReadExtended,
        ]
    ],
    summary="Read user group accessible services",
    description="Retrieve all the services the user group \
        has access to thanks to its SLA. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_user_group_services(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: UserGroup = Depends(valid_user_group_id),
    qservice: ServiceQuery = Depends(),
):
    items = item.services(**qservice.dict(exclude_none=True))
    return service.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )
