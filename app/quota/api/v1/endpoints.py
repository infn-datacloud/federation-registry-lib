from fastapi import APIRouter, Body, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional, Union

from app.pagination import Pagination, paginate
from app.project.api.dependencies import project_has_no_sla
from app.project.models import Project as ProjectModel
from app.query import CommonGetQuery
from app.quota.api.dependencies import valid_quota_id
from app.quota.crud import quota
from app.quota.models import Quota as QuotaModel
from app.quota.schemas import QuotaCreate, QuotaQuery, QuotaUpdate
from app.quota.schemas_extended import (
    NumCPUQuotaReadExtended,
    RAMQuotaReadExtended,
)
from app.service.api.dependencies import valid_service_id
from app.service.models import Service as ServiceModel

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
    "/{quota_uid}",
    status_code=status.HTTP_201_CREATED,
    response_model=Union[NumCPUQuotaReadExtended, RAMQuotaReadExtended],
)
def post_quota(
    project: ProjectModel = Depends(project_has_no_sla),
    service: ServiceModel = Depends(valid_service_id),
    item: QuotaCreate = Body(),
):
    # Check Project provider is one of the UserGroup accessible providers
    provider = project.provider.single()
    idp = user_group.identity_provider.single()
    providers = idp.providers.all()
    if provider not in providers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project's provider {provider} does not support given user group",
        )
    # Check UserGroup does not already have a project on the same provider
    slas = user_group.slas.all()
    for s in slas:
        p = s.project.single()
        if p.provider.single() == provider:
            msg = f"Project's provider {provider} has already assigned "
            msg += f"a project to user group {user_group}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg,
            )
    # Create Quota
    db_obj = quota.create(obj_in=item)
    project.quotas.connect(db_obj)
    # service..connect(db_obj)
    return db_obj


@db.read_transaction
@router.get(
    "/{quota_uid}",
    response_model=Union[NumCPUQuotaReadExtended, RAMQuotaReadExtended],
)
def get_quota(item: QuotaModel = Depends(valid_quota_id)):
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
    item: QuotaModel = Depends(valid_quota_id),
):
    return quota.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{quota_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quotas(item: QuotaModel = Depends(valid_quota_id)):
    if not quota.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
