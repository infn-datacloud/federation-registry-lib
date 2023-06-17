from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/slas", tags=["slas"])


@db.write_transaction
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.SLA
)
def add_sla(item: schemas.SLACreate):
    db_item = crud.get_sla(start_date=item.start_date, end_date=item.end_date)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SLA already registered",
        )
    db_user_group = crud.get_user_group(
        uid=str(item.user_group).replace("-", "")
    )
    if db_user_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="UserGroup not found"
        )
    db_proj = crud.get_project(uid=str(item.project).replace("-", ""))
    if db_proj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    db_provider = db_proj.provider.single()
    services = []
    for service in item.services:
        db_srv = crud.get_service(uid=str(service.uid).replace("-", ""))
        if db_srv is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service {service.name} not found",
            )
        if len(db_srv.providers.all_relationships(db_provider)) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service's provider does not match the project's provider",
            )
        services.append((db_srv, service.relationships))
    db_item = crud.create_sla(
        item, project=db_proj, user_group=db_user_group, services=services
    )
    return db_item


@db.read_transaction
@router.get("/{uid}", response_model=schemas.SLA)
def read_sla(uid: UUID):
    db_item = crud.get_sla(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="SLA not found"
        )
    return db_item


# TODO
@db.write_transaction
@router.patch("/{uid}", response_model=schemas.SLA)
def update_sla(uid: UUID, item: schemas.SLAUpdate):
    db_item = crud.get_sla(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="SLA not found"
        )
    # for service in item.services:
    #    db_srv = crud.get_service(name=service.name)
    #    if db_srv is None:
    #        raise HTTPException(
    #            status_code=status.HTTP_404_NOT_FOUND,
    #            detail=f"Service {service.name} not found",
    #        )
    return crud.update_sla(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slas(uid: UUID):
    db_item = crud.get_sla(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="SLA not found"
        )
    if not crud.remove_sla(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.SLA])
def read_slas(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.UserGroupBase = Depends(),
):
    items = crud.get_slas(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)
