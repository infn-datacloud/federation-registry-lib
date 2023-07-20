from fastapi import APIRouter, Body, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional, Union

from app.pagination import Pagination, paginate
from app.project.api.dependencies import valid_project_id
from app.project.models import Project
from app.query import CommonGetQuery
from app.quota.api.dependencies import valid_quota_id
from app.quota.crud import quota
from app.quota.models import Quota
from app.quota.schemas import (
    NumCPUQuotaCreate,
    QuotaQuery,
    QuotaUpdate,
    RAMQuotaCreate,
)
from app.quota.schemas_extended import (
    NumCPUQuotaReadExtended,
    RAMQuotaReadExtended,
)
from app.service.api.dependencies import valid_service_id
from app.service.models import Service

router = APIRouter(prefix="/quotas", tags=["quotas"])


@db.read_transaction
@router.get(
    "/",
    response_model=List[Union[NumCPUQuotaReadExtended, RAMQuotaReadExtended]],
)
def get_quotas(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: QuotaQuery = Depends(),
):
    items = quota.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Union[NumCPUQuotaReadExtended, RAMQuotaReadExtended],
)
def post_quota(
    project: Project = Depends(valid_project_id),
    service: Service = Depends(valid_service_id),
    item: Union[NumCPUQuotaCreate, RAMQuotaCreate] = Body(),
):
    # Check project does not have duplicated quota types
    for q in project.quotas.all():
        if q.type == item.type and q.service.single() == service:
            msg = f"Project '{project.name}' already has a quota "
            msg += f"with type '{item.type}' on service '{service.endpoint}'."
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=msg
            )
    # Check Project provider and service provider are equals
    proj_prov = project.provider.single()
    serv_prov = service.provider.single()
    if proj_prov != serv_prov:
        msg = f"Project provider '{proj_prov.name}' and service provider "
        msg += f"'{serv_prov.name}' do not match."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=msg
        )

    return quota.create(
        obj_in=item, project=project, service=service, force=True
    )


@db.read_transaction
@router.get(
    "/{quota_uid}",
    response_model=Union[NumCPUQuotaReadExtended, RAMQuotaReadExtended],
)
def get_quota(item: Quota = Depends(valid_quota_id)):
    return item


@db.write_transaction
@router.put(
    "/{quota_uid}",
    response_model=Optional[
        Union[NumCPUQuotaReadExtended, RAMQuotaReadExtended]
    ],
)
def put_quota(
    update_data: QuotaUpdate,
    item: Quota = Depends(valid_quota_id),
):
    return quota.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{quota_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotas(item: Quota = Depends(valid_quota_id)):
    if not quota.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
