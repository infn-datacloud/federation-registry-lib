from typing import List, Optional, Union

from app.auth.dependencies import check_read_access, check_write_access
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.quota.api.dependencies import (
    valid_block_storage_quota_id,
    valid_compute_quota_id,
    validate_new_block_storage_quota_values,
    validate_new_compute_quota_values,
)
from app.quota.crud import block_storage_quota, compute_quota
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.quota.schemas import (
    BlockStorageQuotaQuery,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaReadShort,
    BlockStorageQuotaUpdate,
    ComputeQuotaQuery,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaReadShort,
    ComputeQuotaUpdate,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db

bs_router = APIRouter(prefix="/block_storage_quotas", tags=["block_storage_quotas"])


@db.read_transaction
@bs_router.get(
    "/",
    response_model=Union[
        List[BlockStorageQuotaReadExtended],
        List[BlockStorageQuotaRead],
        List[BlockStorageQuotaReadShort],
        List[BlockStorageQuotaReadExtendedPublic],
        List[BlockStorageQuotaReadPublic],
    ],
    summary="Read all quotas",
    description="Retrieve all quotas stored in the database. \
        It is possible to filter on quotas attributes and other \
        common query parameters.",
)
def get_block_storage_quotas(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: BlockStorageQuotaQuery = Depends(),
):
    items = block_storage_quota.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = block_storage_quota.paginate(items=items, page=page.page, size=page.size)
    return block_storage_quota.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


# @db.write_transaction
# @bs_router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=BlockStorageQuotaReadExtended,
#     dependencies=[Depends(check_write_access)],
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
        BlockStorageQuotaReadShort,
        BlockStorageQuotaReadExtendedPublic,
        BlockStorageQuotaReadPublic,
    ],
    summary="Read a specific quota",
    description="Retrieve a specific quota using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_block_storage_quota(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: BlockStorageQuota = Depends(valid_block_storage_quota_id),
):
    return block_storage_quota.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@bs_router.patch(
    "/{quota_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[BlockStorageQuotaRead],
    dependencies=[
        Depends(check_write_access),
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
def put_block_storage_quota(
    update_data: BlockStorageQuotaUpdate,
    response: Response,
    item: BlockStorageQuota = Depends(valid_block_storage_quota_id),
):
    db_item = block_storage_quota.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@bs_router.delete(
    "/{quota_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific quota",
    description="Delete a specific quota using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
def delete_block_storage_quotas(
    item: BlockStorageQuota = Depends(valid_block_storage_quota_id),
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
        List[ComputeQuotaReadShort],
        List[ComputeQuotaReadExtendedPublic],
        List[ComputeQuotaReadPublic],
    ],
    summary="Read all compute quotas",
    description="Retrieve all compute quotas stored in the database. \
        It is possible to filter on quotas attributes and other \
        common query parameters.",
)
def get_compute_quotas(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: ComputeQuotaQuery = Depends(),
):
    items = compute_quota.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = compute_quota.paginate(items=items, page=page.page, size=page.size)
    return compute_quota.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


# @db.write_transaction
# @c_router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ComputeQuotaReadExtended,
#     dependencies=[Depends(check_write_access)],
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
        ComputeQuotaReadShort,
        ComputeQuotaReadExtendedPublic,
        ComputeQuotaReadPublic,
    ],
    summary="Read a specific quota",
    description="Retrieve a specific quota using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_compute_quota(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: ComputeQuota = Depends(valid_compute_quota_id),
):
    return compute_quota.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@c_router.patch(
    "/{quota_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ComputeQuotaRead],
    dependencies=[
        Depends(check_write_access),
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
def put_compute_quota(
    update_data: ComputeQuotaUpdate,
    response: Response,
    item: ComputeQuota = Depends(valid_compute_quota_id),
):
    db_item = compute_quota.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@c_router.delete(
    "/{quota_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific quota",
    description="Delete a specific quota using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. \
        If the deletion procedure fails, raises a `internal \
        server` error",
)
def delete_compute_quotas(item: ComputeQuota = Depends(valid_compute_quota_id)):
    if not compute_quota.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
