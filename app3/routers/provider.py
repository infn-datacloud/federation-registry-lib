from fastapi import APIRouter, HTTPException
from typing import List, Optional
from neomodel import db

from .. import crud, schemas

router = APIRouter(prefix="/providers", tags=["providers"])


@router.post("/", response_model=schemas.Provider)
def add_provider(item: schemas.ProviderCreate):
    db_item = crud.get_provider(name=item.name)
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_provider(item)


@router.get("/{uid}", response_model=schemas.Provider)
def read_provider(uid: str):
    db_item = crud.get_provider(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_item


@router.get("/", response_model=List[schemas.Provider])
def read_providers(skip: int = 0, limit: int = -1, **kwargs):
    return crud.get_providers(**kwargs)[skip : skip + limit]


@router.delete("/{uid}")
def delete_providers(uid: str) -> bool:
    db_item = crud.get_provider(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return crud.remove_provider(db_item)
