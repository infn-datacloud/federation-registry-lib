from uuid import UUID
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/slas", tags=["slas"])


@router.post("/", response_model=schemas.SLA)
def add_sla(project_id: UUID, provider_id: UUID, item: schemas.SLACreate):
    with db.session() as session:
        db_sla = session.execute_read(crud.get_sla_by_name, name=item.name)
        if db_sla:
            raise HTTPException(
                status_code=400, detail="Name already registered"
            )
        return session.execute_write(
            crud.create_sla,
            project_id=project_id,
            provider_id=provider_id,
            **item.dict(),
        )


@router.get("/{id}", response_model=schemas.SLA)
def read_sla(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_sla, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="SLA not found")
        return item


@router.get("/", response_model=List[schemas.SLA])
def read_slas(
    skip: int = 0,
    limit: int = 100,
    sla_id: Optional[int] = None,
):
    with db.session() as session:
        return session.execute_read(crud.get_slas)


@router.delete("/{id}")
def delete_slas(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_sla, id=id)


@router.post("/{sla_id}/quotas", response_model=schemas.Quota)
def add_quota(sla_id: UUID, item: schemas.QuotaCreate):
    with db.session() as session:
        # db_quota = session.execute_read(crud.get_quota_by_name, name=item.name)
        # if db_quota:
        #    raise HTTPException(
        #        status_code=400, detail="Name already registered"
        #    )
        return session.execute_write(
            crud.create_quota, sla_id=sla_id, **item.dict()
        )


@router.post("/{sla_id}/services", response_model=schemas.Service)
def add_service(sla_id: UUID, item: schemas.ServiceCreate):
    with db.session() as session:
        return session.execute_write(
            crud.create_service, sla_id=sla_id, **item.dict()
        )
