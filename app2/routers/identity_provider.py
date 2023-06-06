from uuid import UUID
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/identity_providers", tags=["identity_providers"])


@router.post("/", response_model=schemas.IdentityProvider)
def add_identity_provider(item: schemas.IdentityProviderCreate):
    with db.session() as session:
        db_identity_provider = session.execute_read(
            crud.get_identity_provider_by_name, name=item.name
        )
        if db_identity_provider:
            raise HTTPException(
                status_code=400, detail="Name already registered"
            )
        return session.execute_write(crud.create_identity_provider, **item.dict())


@router.get("/{id}", response_model=schemas.IdentityProvider)
def read_identity_provider(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_identity_provider, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="IdentityProvider not found")
        return item

@router.get("/", response_model=List[schemas.IdentityProvider])
def read_identity_providers(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
):
    with db.session() as session:
        return session.execute_read(crud.get_identity_providers)


@router.delete("/{id}")
def delete_identity_providers(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_identity_provider, id=id)
