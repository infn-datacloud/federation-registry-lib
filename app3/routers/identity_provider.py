from fastapi import APIRouter, HTTPException
from neomodel import db
from typing import List

from .. import crud, schemas

router = APIRouter(prefix="/identity_providers", tags=["identity_providers"])


@db.write_transaction
@router.post("/", response_model=schemas.IdentityProvider)
def add_identity_provider(item: schemas.IdentityProviderCreate):
    db_item = crud.get_identity_provider(name=item.name)
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_identity_provider(item)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.IdentityProvider)
def read_identity_provider(uid: str):
    db_item = crud.get_identity_provider(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="IdentityProvider not found")
    return db_item

@db.read_transaction
@router.get("/", response_model=List[schemas.IdentityProvider])
def read_identity_providers(skip: int = 0, limit: int = 100):
    return crud.get_identity_providers()[skip : skip + limit]


@db.write_transaction
@router.delete("/{uid}")
def delete_identity_providers(uid: str) -> bool:
    db_item = crud.get_identity_provider(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="IdentityProvider not found")
    return crud.remove_identity_provider(db_item)
