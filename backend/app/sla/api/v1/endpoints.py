from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db
from typing import List, Optional

from app.pagination import Pagination, paginate
from app.project.api.dependencies import project_has_no_sla
from app.project.models import Project
from app.query import CommonGetQuery
from app.sla.api.dependencies import (
    valid_sla_id,
    is_unique_sla,
    validate_new_sla_values,
)
from app.sla.crud import sla
from app.sla.models import SLA
from app.sla.schemas import SLACreate, SLAQuery, SLAUpdate
from app.sla.schemas_extended import SLAReadExtended
from app.user_group.api.dependencies import valid_user_group_id
from app.user_group.models import UserGroup

router = APIRouter(prefix="/slas", tags=["slas"])


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
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SLAReadExtended,
    dependencies=[Depends(is_unique_sla)],
)
def post_sla(
    item: SLACreate,
    project: Project = Depends(project_has_no_sla),
    user_group: UserGroup = Depends(valid_user_group_id),
):
    # Check Project provider is one of the UserGroup accessible providers
    provider = project.provider.single()
    idp = user_group.identity_provider.single()
    providers = idp.providers.all()
    if provider not in providers:
        msg = f"Project's provider '{provider.name}' does not support "
        msg += "given user group."
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=msg
        )
    # Check UserGroup does not already have a project on the same provider
    slas = user_group.slas.all()
    for s in slas:
        p = s.project.single()
        if p.provider.single() == provider:
            msg = f"Project's provider '{provider.name}' has already assigned "
            msg += f"a project to user group '{user_group.name}'."
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=msg
            )
    # Create SLA
    return sla.create(
        obj_in=item, project=project, user_group=user_group, force=True
    )


@db.read_transaction
@router.get("/{sla_uid}", response_model=SLAReadExtended)
def get_sla(item: SLA = Depends(valid_sla_id)):
    return item


@db.write_transaction
@router.put(
    "/{sla_uid}",
    response_model=Optional[SLAReadExtended],
    dependencies=[Depends(validate_new_sla_values)],
)
def put_sla(
    update_data: SLAUpdate,
    response: Response,
    item: SLA = Depends(valid_sla_id),
):
    db_item = sla.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete("/{sla_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slas(item: SLA = Depends(valid_sla_id)):
    if not sla.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
