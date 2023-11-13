from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

from app.auth.dependencies import check_read_access, check_write_access

# from app.identity_provider.crud import identity_provider
# from app.identity_provider.schemas import (
#     IdentityProviderRead,
#     IdentityProviderReadPublic,
#     IdentityProviderReadShort,
# )
# from app.identity_provider.schemas_extended import (
#     IdentityProviderReadExtended,
#     IdentityProviderReadExtendedPublic,
# )
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.service.api.dependencies import (
    valid_block_storage_service_id,
    valid_compute_service_id,
    valid_identity_service_id,
    valid_network_service_id,
    validate_new_block_storage_service_values,
    validate_new_compute_service_values,
    validate_new_identity_service_values,
    validate_new_network_service_values,
)
from app.service.crud import (
    block_storage_service,
    compute_service,
    identity_service,
    network_service,
)
from app.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from app.service.schemas import (
    BlockStorageServiceQuery,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    BlockStorageServiceReadShort,
    BlockStorageServiceUpdate,
    ComputeServiceQuery,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceReadShort,
    ComputeServiceUpdate,
    IdentityServiceQuery,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceReadShort,
    IdentityServiceUpdate,
    NetworkServiceQuery,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    NetworkServiceReadShort,
    NetworkServiceUpdate,
)
from app.service.schemas_extended import (
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
)

bs_router = APIRouter(prefix="/block_storage_services", tags=["block_storage_services"])


@db.read_transaction
@bs_router.get(
    "/",
    response_model=Union[
        List[BlockStorageServiceReadExtended],
        List[BlockStorageServiceRead],
        List[BlockStorageServiceReadShort],
        List[BlockStorageServiceReadExtendedPublic],
        List[BlockStorageServiceReadPublic],
    ],
    summary="Read all BlockStorage services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
def get_block_storage_services(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: BlockStorageServiceQuery = Depends(),
):
    items = block_storage_service.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = block_storage_service.paginate(items=items, page=page.page, size=page.size)
    return block_storage_service.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@bs_router.get(
    "/{service_uid}",
    response_model=Union[
        BlockStorageServiceReadExtended,
        BlockStorageServiceRead,
        BlockStorageServiceReadShort,
        BlockStorageServiceReadExtendedPublic,
        BlockStorageServiceReadPublic,
    ],
    summary="Read a specific BlockStorage service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_block_storage_service(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: BlockStorageService = Depends(valid_block_storage_service_id),
):
    return block_storage_service.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@bs_router.patch(
    "/{service_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[BlockStorageServiceRead],
    dependencies=[
        Depends(check_write_access),
        Depends(validate_new_block_storage_service_values),
    ],
    summary="Edit a specific BlockStorage service",
    description="Update attribute values of a specific service. \
        The target service is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new service values checking there are \
        no other items with the given *endpoint*.",
)
def put_block_storage_service(
    update_data: BlockStorageServiceUpdate,
    response: Response,
    item: BlockStorageService = Depends(valid_block_storage_service_id),
):
    db_item = block_storage_service.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@bs_router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific BlockStorage service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
def delete_block_storage_services(
    item: BlockStorageService = Depends(valid_block_storage_service_id),
):
    if not block_storage_service.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


c_router = APIRouter(prefix="/compute_services", tags=["compute_services"])


@db.read_transaction
@c_router.get(
    "/",
    response_model=Union[
        List[ComputeServiceReadExtended],
        List[ComputeServiceRead],
        List[ComputeServiceReadShort],
        List[ComputeServiceReadExtendedPublic],
        List[ComputeServiceReadPublic],
    ],
    summary="Read all Compute services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
def get_compute_services(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ComputeServiceQuery = Depends(),
):
    items = compute_service.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = compute_service.paginate(items=items, page=page.page, size=page.size)
    return compute_service.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@c_router.get(
    "/{service_uid}",
    response_model=Union[
        ComputeServiceReadExtended,
        ComputeServiceRead,
        ComputeServiceReadShort,
        ComputeServiceReadExtendedPublic,
        ComputeServiceReadPublic,
    ],
    summary="Read a specific Compute service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_compute_service(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: ComputeService = Depends(valid_compute_service_id),
):
    return compute_service.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@c_router.patch(
    "/{service_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ComputeServiceRead],
    dependencies=[
        Depends(check_write_access),
        Depends(validate_new_compute_service_values),
    ],
    summary="Edit a specific Compute service",
    description="Update attribute values of a specific service. \
        The target service is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new service values checking there are \
        no other items with the given *endpoint*.",
)
def put_compute_service(
    update_data: ComputeServiceUpdate,
    response: Response,
    item: ComputeService = Depends(valid_compute_service_id),
):
    db_item = compute_service.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@c_router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific Compute service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
def delete_compute_services(item: ComputeService = Depends(valid_compute_service_id)):
    if not compute_service.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


i_router = APIRouter(prefix="/identity_services", tags=["identity_services"])


@db.read_transaction
@i_router.get(
    "/",
    response_model=Union[
        List[IdentityServiceReadExtended],
        List[IdentityServiceRead],
        List[IdentityServiceReadShort],
        List[IdentityServiceReadExtendedPublic],
        List[IdentityServiceReadPublic],
    ],
    summary="Read all Identity services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
def get_identity_services(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: IdentityServiceQuery = Depends(),
):
    items = identity_service.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = identity_service.paginate(items=items, page=page.page, size=page.size)
    return identity_service.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@i_router.get(
    "/{service_uid}",
    response_model=Union[
        IdentityServiceReadExtended,
        IdentityServiceRead,
        IdentityServiceReadShort,
        IdentityServiceReadExtendedPublic,
        IdentityServiceReadPublic,
    ],
    summary="Read a specific Identity service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_identity_sservice(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: IdentityService = Depends(valid_identity_service_id),
):
    return identity_service.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@i_router.patch(
    "/{service_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[IdentityServiceRead],
    dependencies=[
        Depends(check_write_access),
        Depends(validate_new_identity_service_values),
    ],
    summary="Edit a specific Identity service",
    description="Update attribute values of a specific service. \
        The target service is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new service values checking there are \
        no other items with the given *endpoint*.",
)
def put_identity_sservice(
    update_data: IdentityServiceUpdate,
    response: Response,
    item: IdentityService = Depends(valid_identity_service_id),
):
    db_item = identity_service.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@i_router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific Identity service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
def delete_identity_sservices(
    item: IdentityService = Depends(valid_identity_service_id),
):
    if not identity_service.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


n_router = APIRouter(prefix="/network_services", tags=["network_services"])


@db.read_transaction
@n_router.get(
    "/",
    response_model=Union[
        List[NetworkServiceReadExtended],
        List[NetworkServiceRead],
        List[NetworkServiceReadShort],
        List[NetworkServiceReadExtendedPublic],
        List[NetworkServiceReadPublic],
    ],
    summary="Read all Network services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
def get_network_services(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: NetworkServiceQuery = Depends(),
):
    items = network_service.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = network_service.paginate(items=items, page=page.page, size=page.size)
    return network_service.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@n_router.get(
    "/{service_uid}",
    response_model=Union[
        NetworkServiceReadExtended,
        NetworkServiceRead,
        NetworkServiceReadShort,
        NetworkServiceReadExtendedPublic,
        NetworkServiceReadPublic,
    ],
    summary="Read a specific Network service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_network_service(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: NetworkService = Depends(valid_network_service_id),
):
    return network_service.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@n_router.patch(
    "/{service_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[NetworkServiceRead],
    dependencies=[
        Depends(check_write_access),
        Depends(validate_new_network_service_values),
    ],
    summary="Edit a specific Network service",
    description="Update attribute values of a specific service. \
        The target service is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message. \
        At first validate new service values checking there are \
        no other items with the given *endpoint*.",
)
def put_network_service(
    update_data: NetworkServiceUpdate,
    response: Response,
    item: NetworkService = Depends(valid_network_service_id),
):
    db_item = network_service.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@n_router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific Network service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
def delete_network_services(item: NetworkService = Depends(valid_network_service_id)):
    if not network_service.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


# @db.read_transaction
# @router.get(
#     "/{service_uid}/identity_providers",
#     response_model=Union[
#         List[IdentityProviderReadExtended],
#         List[IdentityProviderRead],
#         List[IdentityProviderReadShort],
#         List[IdentityProviderReadExtendedPublic],
#         List[IdentityProviderReadPublic],
#     ],
#     summary="Read service accessible identity providers",
#     description="Retrieve all the identity providers the \
#         service has access to. \
#         If no entity matches the given *uid*, the endpoint \
#         raises a `not found` error.",
# )
# def get_service_identity_providers(
#     auth: bool = Depends(check_read_access),
#     size: SchemaSize = Depends(),
#     item: Service = Depends(valid_service_id),
# ):
#     items = item.provider.single().identity_providers.all()
#     return identity_provider.choose_out_schema(
#         items=items, auth=auth, short=size.short, with_conn=size.with_conn
#     )
