from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List

from .crud import create_sla, edit_sla, read_slas, remove_sla
from .dependencies import valid_sla_id
from .models import SLA as SLAModel
from .schemas import SLACreateExtended, SLAPatch, SLAQuery, SLA
from ..pagination import Pagination, paginate
from ..project.dependencies import valid_project_id
from ..quota.dependencies import validate_quota
from ..quota.schemas import QuotaCreateExtended
from ..query import CommonGetQuery
from ..service.dependencies import valid_service_id
from ..user_group.dependencies import valid_user_group_id


router = APIRouter(prefix="/slas", tags=["slas"])


@db.read_transaction
@router.get("/", response_model=List[SLA])
def get_slas(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: SLAQuery = Depends(),
):
    items = read_slas(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SLA)
def post_sla(item: SLACreateExtended):
    project = valid_project_id(item.project_uid)
    user_group = valid_user_group_id(item.user_group_uid)
    if project.sla.single():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project {item.project_uid} already has an associated SLA",
        )
    provider = project.provider.single()
    quotas = []
    for quota in item.quotas:
        service = valid_service_id(quota.service_uid)
        quota = validate_quota(quota, service)
        if service.provider.single().name != provider.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quota '{quota.type.name}' refers to a service belonging to a provider different from the project's one",
            )
        quotas.append(QuotaCreateExtended(**quota.dict(), service=service))
    return create_sla(
        item=item, project=project, user_group=user_group, quotas=quotas
    )


@db.read_transaction
@router.get("/{sla_uid}", response_model=SLA)
def get_sla(item: SLAModel = Depends(valid_sla_id)):
    return item


# TODO
@db.write_transaction
@router.patch("/{sla_uid}", response_model=SLA)
def patch_sla(update_data: SLAPatch, item: SLAModel = Depends(valid_sla_id)):
    # for service in item.services:
    #    db_srv = get_service(name=service.name)
    #    if db_srv is None:
    #        raise HTTPException(
    #            status_code=status.HTTP_404_NOT_FOUND,
    #            detail=f"Service {service.name} not found",
    #        )
    return edit_sla(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{sla_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slas(item: SLAModel = Depends(valid_sla_id)):
    if not remove_sla(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
