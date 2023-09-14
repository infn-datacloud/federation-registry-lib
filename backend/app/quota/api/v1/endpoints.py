from typing import List, Optional, Union

from app.auth.dependencies import check_read_access, check_write_access
from app.project.api.dependencies import valid_project_id
from app.project.models import Project
from app.query import DbQueryCommonParams, Pagination, SchemaSize
from app.quota.api.dependencies import valid_quota_id
from app.quota.crud import quota
from app.quota.models import CinderQuota, NovaQuota
from app.quota.schemas import (
    CinderQuotaCreate,
    CinderQuotaQuery,
    CinderQuotaRead,
    CinderQuotaReadPublic,
    CinderQuotaReadShort,
    CinderQuotaUpdate,
    NovaQuotaCreate,
    NovaQuotaQuery,
    NovaQuotaRead,
    NovaQuotaReadPublic,
    NovaQuotaReadShort,
    NovaQuotaUpdate,
)
from app.quota.schemas_extended import (
    CinderQuotaReadExtended,
    CinderQuotaReadExtendedPublic,
    NovaQuotaReadExtended,
    NovaQuotaReadExtendedPublic,
)
from app.service.api.dependencies import valid_service_id
from app.service.models import Service
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from neomodel import db

router = APIRouter(prefix="/quotas", tags=["quotas"])


@db.read_transaction
@router.get(
    "/",
    response_model=Union[
        List[Union[NovaQuotaReadExtended, CinderQuotaReadExtended]],
        List[Union[NovaQuotaRead, CinderQuotaRead]],
        List[Union[NovaQuotaReadShort, CinderQuotaReadShort]],
        List[Union[NovaQuotaReadExtendedPublic, CinderQuotaReadExtendedPublic]],
        List[Union[NovaQuotaReadPublic, CinderQuotaReadPublic]],
    ],
    summary="Read all quotas",
    description="Retrieve all quotas stored in the database. \
        It is possible to filter on quotas attributes and other \
        common query parameters.",
)
def get_quotas(
    auth: bool = Depends(check_read_access),
    comm: DbQueryCommonParams = Depends(),
    page: Pagination = Depends(),
    size: SchemaSize = Depends(),
    item: Union[NovaQuotaQuery, CinderQuotaQuery] = Depends(),
):
    items = quota.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    items = quota.paginate(items=items, page=page.page, size=page.size)
    return quota.choose_out_schema(
        items=items, auth=auth, short=size.short, with_conn=size.with_conn
    )


@db.write_transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Union[NovaQuotaReadExtended, CinderQuotaReadExtended],
    dependencies=[Depends(check_write_access)],
    summary="Create quota",
    description="Create a quota and connect it to its related entities: \
        project and service. \
        At first verify that target project and service exist. \
        Then verify project does not already have an equal quota type and \
        check service and project belong to the same provider.",
)
def post_quota(
    project: Project = Depends(valid_project_id),
    service: Service = Depends(valid_service_id),
    item: Union[NovaQuotaCreate, CinderQuotaCreate] = Body(),
):
    # Check project does not have duplicated quota types
    for q in project.quotas.all():
        if q.type == item.type and q.service.single() == service:
            msg = f"Project '{project.name}' already has a quota "
            msg += f"with type '{item.type}' on service '{service.endpoint}'."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    # Check Project provider and service provider are equals
    proj_prov = project.provider.single()
    serv_prov = service.provider.single()
    if proj_prov != serv_prov:
        msg = f"Project provider '{proj_prov.name}' and service provider "
        msg += f"'{serv_prov.name}' do not match."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    return quota.create(obj_in=item, project=project, service=service, force=True)


@db.read_transaction
@router.get(
    "/{quota_uid}",
    response_model=Union[
        NovaQuotaReadExtended,
        CinderQuotaReadExtended,
        NovaQuotaRead,
        CinderQuotaRead,
        NovaQuotaReadShort,
        CinderQuotaReadShort,
        NovaQuotaReadExtendedPublic,
        CinderQuotaReadExtendedPublic,
        NovaQuotaReadPublic,
        CinderQuotaReadPublic,
    ],
    summary="Read a specific quota",
    description="Retrieve a specific quota using its *uid*. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def get_quota(
    auth: bool = Depends(check_read_access),
    size: SchemaSize = Depends(),
    item: Union[NovaQuotaCreate, CinderQuotaCreate] = Depends(valid_quota_id),
):
    return quota.choose_out_schema(
        items=[item], auth=auth, short=size.short, with_conn=size.with_conn
    )[0]


@db.write_transaction
@router.patch(
    "/{quota_uid}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[Union[NovaQuotaRead, CinderQuotaRead]],
    dependencies=[Depends(check_write_access)],
    summary="Edit a specific quota",
    description="Update attribute values of a specific quota. \
        The target quota is identified using its uid. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error. If new values equal \
        current ones, the database entity is left unchanged \
        and the endpoint returns the `not modified` message.",
)
def put_quota(
    update_data: Union[NovaQuotaUpdate, CinderQuotaUpdate],
    response: Response,
    item: Union[NovaQuota, CinderQuota] = Depends(valid_quota_id),
):
    db_item = quota.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete(
    "/{quota_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(check_write_access)],
    summary="Delete a specific quota",
    description="Delete a specific quota using its *uid*. \
        Returns `no content`. \
        If no entity matches the given *uid*, the endpoint \
        raises a `not found` error.",
)
def delete_quotas(item: Union[NovaQuota, CinderQuota] = Depends(valid_quota_id)):
    if not quota.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
