from fastapi import APIRouter, HTTPException
from neomodel import db
from typing import List

from .. import crud, schemas

router = APIRouter(prefix="/slas", tags=["slas"])


@db.write_transaction
@router.post("/", response_model=schemas.SLA)
def add_sla(project_id: str, provider_id: str, item: schemas.SLACreate):
    db_provider = crud.get_provider(uid=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    db_project = crud.get_project(uid=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db_item = crud.get_sla(name=item.name)
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Name already registered")
    db_sla = crud.create_sla(item=item)
    if not crud.connect_sla_to_project_and_provider(
        sla=db_sla, db_provider=db_provider, project=db_project
    ):
        raise HTTPException(
            status_code=500, detail="Relationship creation failed"
        )
    return db_sla


@db.read_transaction
@router.get("/{uid}", response_model=schemas.SLA)
def read_sla(uid: str):
    db_item = crud.get_sla(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="SLA not found")
    return db_item


@db.read_transaction
@router.get("/", response_model=List[schemas.SLA])
def read_slas(skip: int = 0, limit: int = 100):
    return crud.get_slas()[skip : skip + limit]


@db.write_transaction
@router.delete("/{uid}")
def delete_slas(uid: str) -> bool:
    db_item = crud.get_sla(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="SLA not found")
    return crud.remove_sla(db_item)


@db.write_transaction
@router.post("/{uid}/quotas", response_model=schemas.Quota)
def add_quota_to_sla(uid: str, item: schemas.QuotaCreate):
    db_sla = crud.get_sla(uid=uid)
    if db_sla is None:
        raise HTTPException(status_code=404, detail="SLA not found")
    db_quota = crud.create_quota(item=item)
    if not crud.connect_quota_to_sla(sla=db_sla, quota=db_quota):
        raise HTTPException(
            status_code=500, detail="Relationship creation failed"
        )
    return db_quota


@db.write_transaction
@router.post("/{uid}/services", response_model=schemas.Service)
def add_service_to_sla(uid: str, item: schemas.ServiceCreate):
    db_sla = crud.get_sla(uid=uid)
    if db_sla is None:
        raise HTTPException(status_code=404, detail="SLA not found")
    db_service = crud.create_service(item=item)
    if not crud.connect_service_to_sla(sla=db_sla, service=db_service):
        raise HTTPException(
            status_code=500, detail="Relationship creation failed"
        )
    return db_service