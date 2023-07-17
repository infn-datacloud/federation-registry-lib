from fastapi import APIRouter, Body, Depends, HTTPException, status
from neomodel import db
from typing import List, Tuple

from ...crud import sla
from ..dependencies import valid_sla_id
from ...models import SLA as SLAModel
from ...schemas import SLACreate,  SLAQuery, SLAUpdate
from ...schemas_extended import SLAReadExtended
from ....pagination import Pagination, paginate
from ....project.models import Project as ProjectModel
from ....project.api.dependencies import project_has_no_sla
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


def providers_match(
    quota_type: QuotaTypeModel, service: ServiceModel, provider: ProviderModel
) -> None:
    if service.provider.single().name != provider.name:
        msg = f"Quota '{quota_type.name}' refers to a service belonging to "
        msg += "a provider different from the project's one"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


def validate_quota(
    quota_type: QuotaTypeCreate,
    service: ServiceCreate,
) -> Tuple[QuotaTypeModel, ServiceModel]:
    qt = valid_quota_type_name(quota_type)
    srv = valid_service_endpoint(service)
    return qt, srv


def user_group_not_linked_to_provider(
    user_group: UserGroupModel, provider: ProviderModel
) -> None:
    for single_sla in user_group.slas.all():
        project = single_sla.project.single()
        if project.provider.single() == provider:
            msg = "User Group already has a dedicated project "
            msg += f"on provider '{provider.name}'"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg,
            )


@db.read_transaction
@router.get("/", response_model=List[SLAReadExtended])
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
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=SLAReadExtended
)
def post_sla(
    project: ProjectModel = Depends(project_has_no_sla),
    user_group: UserGroupModel = Depends(valid_user_group_id),
    item: SLACreate = Body(),
):
    provider = project.provider.single()
    user_group_not_linked_to_provider(user_group, provider)
    quotas = []
    for quota in item.quotas:
        (quota_type, service) = validate_quota(quota.type, quota.service)
        providers_match(quota_type, service, provider)
        quotas.append((quota, quota_type, service))
    return sla.create_with_all(
        sla=item, project=project, user_group=user_group, quotas=quotas
    )


@db.read_transaction
@router.get("/{sla_uid}", response_model=SLAReadExtended)
def get_sla(item: SLAModel = Depends(valid_sla_id)):
    return item


# TODO
@db.write_transaction
@router.put("/{sla_uid}", response_model=SLAReadExtended)
def put_sla(update_data: SLAUpdate, item: SLAModel = Depends(valid_sla_id)):
    # for service in item.services:
    #    db_srv = get_service(name=service.name)
    #    if db_srv is None:
    #        raise HTTPException(
    #            status_code=status.HTTP_404_NOT_FOUND,
    #            detail=f"Service {service.name} not found",
    #        )
    return sla.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{sla_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slas(item: SLAModel = Depends(valid_sla_id)):
    if not sla.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
