from uuid import UUID
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/providers", tags=["providers"])


@router.post("/", response_model=schemas.Provider)
def add_provider(item: schemas.ProviderCreate):
    with db.session() as session:
        db_provider = session.execute_read(
            crud.get_provider_by_name, name=item.name
        )
        if db_provider:
            raise HTTPException(
                status_code=400, detail="Name already registered"
            )
        return session.execute_write(crud.create_provider, **item.dict())


@router.get("/{id}", response_model=schemas.Provider)
def read_provider(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_provider, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="Provider not found")
        return item


@router.get("/", response_model=List[schemas.Provider])
def read_providers(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
):
    with db.session() as session:
        return session.execute_read(crud.get_providers)


@router.delete("/{id}")
def delete_providers(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_provider, id=id)
