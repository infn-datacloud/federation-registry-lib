from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping

from pydantic import UUID4

from .crud import create_sla, edit_sla, read_slas, remove_sla
from .dependencies import valid_sla_id, validate_sla_entities
from .schemas import SLACreate, SLAPatch, SLAQuery, SLA
from ..pagination import Pagination, paginate
from ..query import CommonGetQuery


from ..project.dependencies import valid_project_id
from ..project.models import Project
from ..user_group.dependencies import valid_user_group_id
from ..user_group.models import UserGroup


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
def post_sla(item: SLACreate = Depends(validate_sla_entities)):

#    db_provider = db_proj.provider.single()
#    quotas = []
#    for quota in item.quotas:
#        # TODO Check srv provider match proj one
#        db_quota = create_quota(quota)
#        quotas.append(db_quota)
#    db_item = create_sla(
#        item, project=db_proj, user_group=db_user_group, quotas=quotas
#    )
#   return db_item
    pass

@db.read_transaction
@router.get("/{sla_uid}", response_model=SLA)
def get_sla(item: Mapping = Depends(valid_sla_id)):
    return item


# TODO
@db.write_transaction
@router.patch("/{sla_uid}", response_model=SLA)
def patch_sla(update_data: SLAPatch, item: Mapping = Depends(valid_sla_id)):
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
def delete_slas(item: Mapping = Depends(valid_sla_id)):
    if not remove_sla(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
