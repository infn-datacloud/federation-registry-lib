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
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.quota.api.dependencies import (
    valid_block_storage_quota_id,
    valid_compute_quota_id,
    valid_network_quota_id,
    validate_new_block_storage_quota_values,
    validate_new_compute_quota_values,
    validate_new_network_quota_values,
)
from app.quota.crud import block_storage_quota, compute_quota, network_quota
from app.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from app.quota.schemas import (
    BlockStorageQuotaQuery,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaUpdate,
    ComputeQuotaQuery,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaUpdate,
    NetworkQuotaQuery,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    NetworkQuotaUpdate,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
)

bs_router = APIRouter(prefix="/block_storage_quotas", tags=["block_storage_quotas"])


@db.read_transaction
@bs_router.get(
    "/",
    response_model=Union[
        List[BlockStorageQuotaReadExtended],
        List[BlockStorageQuotaRead],
        List[BlockStorageQuotaReadExtendedPublic],
        List[BlockStorageQuotaReadPublic],
    ],
    summary="Read all quotas",
    description="Retrieve all quotas stored in the database. \
        It is possible to filter on quotas attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_block_storage_quotas(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: BlockStorageQuotaQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = block_storage_quota.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = block_storage_quota.paginate(items=items, page=page.page, size=page.size)
    return block_storage_quota.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


# @db.write_transaction
# @bs_router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=BlockStorageQuotaReadExtended,
#
#     summary="Create quota",
#     description="Create a quota and connect it to its related entities: \
#         project and service. \
#         At first verify that target project and service exist. \
#         Then verify project does not already have an equal quota type and \
#         check service and project belong to the same provider.",
# )
# def post_block_storage_quota(
#     project: Project = Depends(valid_project_id),
#     service: Service = Depends(valid_service_id),
#     item: BlockStorageQuotaCreate = Body(),
# ):
#     # Check project does not have duplicated quota types
#     # for q in project.quotas.all():
#     #     if q.type == item.type and q.service.single() == service:
#     #         msg = f"Project '{project.name}' already has a quota "
#     #         msg += f"with type '{item.type}' on service '{service.endpoint}'."
#     #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
#     # Check Project provider and service provider are equals
#     proj_prov = project.provider.single()
#     serv_prov = service.provider.single()
#     if proj_prov != serv_prov:
#         msg = f"Project provider '{proj_prov.name}' and service provider "
#         msg += f"'{serv_prov.name}' do not match."
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

#     return block_storage_quota.create(
#         obj_in=item, project=project, service=service, force=True
#     )


@db.read_transaction
@bs_router.get(
    "/{quota_uid}",
    response_model=Union[
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaRead,
        BlockStorageQuotaReadExtendedPublic,
        BlockStorageQuotaReadPublic,
    ],
    summary="Read a specific quota",
    description="Retrieve a specific quota using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_block_storage_quota(
    size: SchemaSize = Depends(),
    item: BlockStorageQuota = Depends(valid_block_storage_quota_id),
    user_infos: Optional[Any] = None,
):
    return block_storage_quota.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@bs_router.patch(
    "/{quota_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[BlockStorageQuotaRead],
    dependencies=[
        Depends(validate_new_block_storage_quota_values),
    ],
    summary="Edit a specific quota",
    description="Update attribute values of a specific quota. \
        The target quota is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message.",
)
@flaat.access_level("write")
def put_block_storage_quota(
    request: Request,
    update_data: BlockStorageQuotaUpdate,
    response: Response,
    item: BlockStorageQuota = Depends(valid_block_storage_quota_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = block_storage_quota.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@bs_router.delete(
    "/{quota_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific quota",
    description="Delete a specific quota using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_block_storage_quotas(
    request: Request,
    item: BlockStorageQuota = Depends(valid_block_storage_quota_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not block_storage_quota.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


c_router = APIRouter(prefix="/compute_quotas", tags=["compute_quotas"])


@db.read_transaction
@c_router.get(
    "/",
    response_model=Union[
        List[ComputeQuotaReadExtended],
        List[ComputeQuotaRead],
        List[ComputeQuotaReadExtendedPublic],
        List[ComputeQuotaReadPublic],
    ],
    summary="Read all compute quotas",
    description="Retrieve all compute quotas stored in the database. \
        It is possible to filter on quotas attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_compute_quotas(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ComputeQuotaQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = compute_quota.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = compute_quota.paginate(items=items, page=page.page, size=page.size)
    return compute_quota.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


# @db.write_transaction
# @c_router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ComputeQuotaReadExtended,
#
#     summary="Create compute quota",
#     description="Create a compute quota and connect it to its related entities: \
#         project and service. \
#         At first verify that target project and service exist. \
#         Then verify project does not already have an equal quota type and \
#         check service and project belong to the same provider.",
# )
# def post_compute_quota(
#     project: Project = Depends(valid_project_id),
#     service: Service = Depends(valid_service_id),
#     item: ComputeQuotaCreate = Body(),
# ):
#     # Check project does not have duplicated quota types
#     # for q in project.quotas.all():
#     #     if q.type == item.type and q.service.single() == service:
#     #         msg = f"Project '{project.name}' already has a quota "
#     #         msg += f"with type '{item.type}' on service '{service.endpoint}'."
#     #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
#     # Check Project provider and service provider are equals
#     proj_prov = project.provider.single()
#     serv_prov = service.provider.single()
#     if proj_prov != serv_prov:
#         msg = f"Project provider '{proj_prov.name}' and service provider "
#         msg += f"'{serv_prov.name}' do not match."
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

#     return compute_quota.create(
#         obj_in=item, project=project, service=service, force=True
#     )


@db.read_transaction
@c_router.get(
    "/{quota_uid}",
    response_model=Union[
        ComputeQuotaReadExtended,
        ComputeQuotaRead,
        ComputeQuotaReadExtendedPublic,
        ComputeQuotaReadPublic,
    ],
    summary="Read a specific quota",
    description="Retrieve a specific quota using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_compute_quota(
    size: SchemaSize = Depends(),
    item: ComputeQuota = Depends(valid_compute_quota_id),
    user_infos: Optional[Any] = None,
):
    return compute_quota.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@c_router.patch(
    "/{quota_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ComputeQuotaRead],
    dependencies=[
        Depends(validate_new_compute_quota_values),
    ],
    summary="Edit a specific quota",
    description="Update attribute values of a specific quota. \
        The target quota is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message.",
)
@flaat.access_level("write")
def put_compute_quota(
    request: Request,
    update_data: ComputeQuotaUpdate,
    response: Response,
    item: ComputeQuota = Depends(valid_compute_quota_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = compute_quota.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@c_router.delete(
    "/{quota_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific quota",
    description="Delete a specific quota using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_compute_quotas(
    request: Request,
    item: ComputeQuota = Depends(valid_compute_quota_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not compute_quota.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


n_router = APIRouter(prefix="/network_quotas", tags=["network_quotas"])


@db.read_transaction
@n_router.get(
    "/",
    response_model=Union[
        List[NetworkQuotaReadExtended],
        List[NetworkQuotaRead],
        List[NetworkQuotaReadExtendedPublic],
        List[NetworkQuotaReadPublic],
    ],
    summary="Read all network quotas",
    description="Retrieve all network quotas stored in the database. \
        It is possible to filter on quotas attributes and other \
        common query parameters.",
)
@flaat.inject_user_infos(strict=False)
def get_network_quotas(
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: NetworkQuotaQuery = Depends(),
    user_infos: Optional[Any] = None,
):
    items = network_quota.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = network_quota.paginate(items=items, page=page.page, size=page.size)
    return network_quota.choose_out_schema(
        items=items, auth=user_infos, short=size.short, with_conn=size.with_conn
    )


@db.read_transaction
@n_router.get(
    "/{quota_uid}",
    response_model=Union[
        NetworkQuotaReadExtended,
        NetworkQuotaRead,
        NetworkQuotaReadExtendedPublic,
        NetworkQuotaReadPublic,
    ],
    summary="Read a specific quota",
    description="Retrieve a specific quota using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
@flaat.inject_user_infos(strict=False)
def get_network_quota(
    size: SchemaSize = Depends(),
    item: NetworkQuota = Depends(valid_network_quota_id),
    user_infos: Optional[Any] = None,
):
    return network_quota.choose_out_schema(
        items=[item], auth=user_infos, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@n_router.patch(
    "/{quota_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[NetworkQuotaRead],
    dependencies=[
        Depends(validate_new_network_quota_values),
    ],
    summary="Edit a specific quota",
    description="Update attribute values of a specific quota. \
        The target quota is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message.",
)
@flaat.access_level("write")
def put_network_quota(
    request: Request,
    update_data: NetworkQuotaUpdate,
    response: Response,
    item: NetworkQuota = Depends(valid_network_quota_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    db_item = network_quota.update(db_obj=item, obj_in=update_data)
    if not db_item:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@n_router.delete(
    "/{quota_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific quota",
    description="Delete a specific quota using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
@flaat.access_level("write")
def delete_network_quotas(
    request: Request,
    item: NetworkQuota = Depends(valid_network_quota_id),
    client_credentials: HTTPBasicCredentials = Security(security),
):
    if not network_quota.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
