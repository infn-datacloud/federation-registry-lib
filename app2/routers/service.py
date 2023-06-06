from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/{id}", response_model=schemas.Service)
def read_services(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_service, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="Service not found")
        return item


@router.get("/", response_model=List[schemas.Service])
def read_services():
    with db.session() as session:
        return session.execute_read(crud.get_services)


@router.delete("/{id}")
def delete_services(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_service, id=id)
