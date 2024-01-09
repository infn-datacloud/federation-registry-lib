"""Services endpoints to execute POST, GET, PUT, PATCH and DELETE operations.

They are divided into BlockStorage, Compute, Identity and Network services.
"""
from typing import Any, List, Optional, Union

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
    block_storage_service_mng,
    compute_service_mng,
    identity_service_mng,
    network_service_mng,
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
    BlockStorageServiceUpdate,
    ComputeServiceQuery,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceUpdate,
    IdentityServiceQuery,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceUpdate,
    NetworkServiceQuery,
    NetworkServiceRead,
    NetworkServiceReadPublic,
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
        List[BlockStorageServiceReadExtendedPublic],
        List[BlockStorageServiceReadPublic],
    ],
    summary="Read all BlockStorage services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_block_storage_services(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: BlockStorageServiceQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = block_storage_service_mng.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = block_storage_service_mng.paginate(
        items=items, page=page.page, size=page.size
    )
    return block_storage_service_mng.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@bs_router.get(
    "/{service_uid}",
    response_model=Union[
        BlockStorageServiceReadExtended,
        BlockStorageServiceRead,
        BlockStorageServiceReadExtendedPublic,
        BlockStorageServiceReadPublic,
    ],
    summary="Read a specific BlockStorage service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_block_storage_service(
    size: SchemaSize = Depends(),
    item: BlockStorageService = Depends(valid_block_storage_service_id),
    user_infos: Optional[Any] = None,
):
    return block_storage_service_mng.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@bs_router.patch(
    "/{service_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[BlockStorageServiceRead],
    dependencies=[
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
@flaat.access_level("write")
def put_block_storage_service(
    request: Request,
    update_data: BlockStorageServiceUpdate,
    response: Response,
    item: BlockStorageService = Depends(valid_block_storage_service_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = block_storage_service_mng.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@bs_router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific BlockStorage service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_block_storage_services(
    request: Request,
    item: BlockStorageService = Depends(valid_block_storage_service_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not block_storage_service_mng.remove(db_obj=item):
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
        List[ComputeServiceReadExtendedPublic],
        List[ComputeServiceReadPublic],
    ],
    summary="Read all Compute services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_compute_services(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ComputeServiceQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = compute_service_mng.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = compute_service_mng.paginate(items=items, page=page.page, size=page.size)
    return compute_service_mng.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@c_router.get(
    "/{service_uid}",
    response_model=Union[
        ComputeServiceReadExtended,
        ComputeServiceRead,
        ComputeServiceReadExtendedPublic,
        ComputeServiceReadPublic,
    ],
    summary="Read a specific Compute service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_compute_service(
    size: SchemaSize = Depends(),
    item: ComputeService = Depends(valid_compute_service_id),
    user_infos: Optional[Any] = None,
):
    return compute_service_mng.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@c_router.patch(
    "/{service_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ComputeServiceRead],
    dependencies=[
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
@flaat.access_level("write")
def put_compute_service(
    request: Request,
    update_data: ComputeServiceUpdate,
    response: Response,
    item: ComputeService = Depends(valid_compute_service_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = compute_service_mng.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@c_router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific Compute service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_compute_services(
    request: Request,
    item: ComputeService = Depends(valid_compute_service_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not compute_service_mng.remove(db_obj=item):
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
        List[IdentityServiceReadExtendedPublic],
        List[IdentityServiceReadPublic],
    ],
    summary="Read all Identity services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_identity_services(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: IdentityServiceQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = identity_service_mng.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = identity_service_mng.paginate(items=items, page=page.page, size=page.size)
    return identity_service_mng.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@i_router.get(
    "/{service_uid}",
    response_model=Union[
        IdentityServiceReadExtended,
        IdentityServiceRead,
        IdentityServiceReadExtendedPublic,
        IdentityServiceReadPublic,
    ],
    summary="Read a specific Identity service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_identity_service(
    size: SchemaSize = Depends(),
    item: IdentityService = Depends(valid_identity_service_id),
    user_infos: Optional[Any] = None,
):
    return identity_service_mng.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@i_router.patch(
    "/{service_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[IdentityServiceRead],
    dependencies=[
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
@flaat.access_level("write")
def put_identity_service(
    request: Request,
    update_data: IdentityServiceUpdate,
    response: Response,
    item: IdentityService = Depends(valid_identity_service_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = identity_service_mng.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@i_router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific Identity service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_identity_services(
    request: Request,
    item: IdentityService = Depends(valid_identity_service_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not identity_service_mng.remove(db_obj=item):
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
        List[NetworkServiceReadExtendedPublic],
        List[NetworkServiceReadPublic],
    ],
    summary="Read all Network services",
    description="Retrieve all services stored in the database. \
        It is possible to filter on services attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_network_services(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: NetworkServiceQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = network_service_mng.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = network_service_mng.paginate(items=items, page=page.page, size=page.size)
    return network_service_mng.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@n_router.get(
    "/{service_uid}",
    response_model=Union[
        NetworkServiceReadExtended,
        NetworkServiceRead,
        NetworkServiceReadExtendedPublic,
        NetworkServiceReadPublic,
    ],
    summary="Read a specific Network service",
    description="Retrieve a specific service using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_network_service(
    size: SchemaSize = Depends(),
    item: NetworkService = Depends(valid_network_service_id),
    user_infos: Optional[Any] = None,
):
    return network_service_mng.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@n_router.patch(
    "/{service_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[NetworkServiceRead],
    dependencies=[
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
@flaat.access_level("write")
def put_network_service(
    request: Request,
    update_data: NetworkServiceUpdate,
    response: Response,
    item: NetworkService = Depends(valid_network_service_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = network_service_mng.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@n_router.delete(
    "/{service_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific Network service",
    description="Delete a specific service using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        On cascade, delete related quotas. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_network_services(
    request: Request,
    item: NetworkService = Depends(valid_network_service_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not network_service_mng.remove(db_obj=item):
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
#         items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
#     )
