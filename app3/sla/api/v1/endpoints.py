from fastapi import APIRouter, Body, Depends, HTTPException, status
from neomodel import db
from typing import List, Tuple

from ...crud import sla
from ..dependencies import valid_sla_id
from ...models import SLA as SLAModel
from ...schemas import SLAPatch, SLAQuery, SLA
from ...schemas_extended import SLACreateExtended
from ....pagination import Pagination, paginate
from ....project.models import Project as ProjectModel
from ....project.api.dependencies import valid_project_id
from ....query import CommonGetQuery
from ....user_group.models import UserGroup as UserGroupModel
from ....user_group.api.dependencies import valid_user_group_id

from ....provider.models import Provider as ProviderModel
from ....quota_type.crud import quota_type
from ....quota_type.models import QuotaType as QuotaTypeModel
from ....quota_type.schemas import QuotaTypeCreate
from ....service.crud import service
from ....service.models import Service as ServiceModel
from ....service.schemas import ServiceCreate
from ....service_type.models import ServiceType as ServiceTypeModel

router = APIRouter(prefix="/slas", tags=["slas"])


def valid_service_endpoint(srv: ServiceCreate) -> ServiceModel:
    item = service.get(endpoint=srv.endpoint)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service {srv.endpoint} not found",
        )
    return item


def valid_quota_type_name(qt: QuotaTypeCreate) -> QuotaTypeModel:
    item = quota_type.get(name=qt.name)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quota Type {qt.name} not found",
        )
    return item


def is_allowed_quota_type(
    quota_type: QuotaTypeModel, service_type: ServiceTypeModel
) -> None:
    allowed_quota_types = [t.name for t in service_type.quota_types.all()]
    if quota_type.name not in allowed_quota_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quota '{quota_type.name}' can't be applied on services of type '{service_type}'",
        )


def providers_match(
    quota_type: QuotaTypeModel, service: ServiceModel, provider: ProviderModel
) -> None:
    if service.provider.single().name != provider.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quota '{quota_type.name}' refers to a service belonging to a provider different from the project's one",
        )


def validate_quota(
    quota_type: QuotaTypeCreate,
    service: ServiceCreate,
) -> Tuple[QuotaTypeModel, ServiceModel]:
    qt = valid_quota_type_name(quota_type)
    srv = valid_service_endpoint(service)
    is_allowed_quota_type(qt, srv.type.single())
    return qt, srv


@db.read_transaction
@router.get("/", response_model=List[SLA])
def get_slas(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: SLAQuery = Depends(),
):
    items = sla.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SLA)
def post_sla(
    project: ProjectModel = Depends(valid_project_id),
    user_group: UserGroupModel = Depends(valid_user_group_id),
    item: SLACreateExtended = Body(),
):
    provider = project.provider.single()
    l = []
    for quota in item.quotas:
        (quota_type, service) = validate_quota(quota.type, quota.service)
        providers_match(quota_type, service, provider)
        l.append((quota, quota_type, service))
    return sla.create_with_all(
        sla=item, project=project, user_group=user_group, quotas=l
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
    return sla.update(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{sla_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slas(item: SLAModel = Depends(valid_sla_id)):
    if not sla.remove(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
