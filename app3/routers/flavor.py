from fastapi import APIRouter, HTTPException
from neomodel import db
from typing import List

from .. import crud, schemas

router = APIRouter(prefix="/flavors", tags=["flavors"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Flavor)
def read_flavor(uid: str):
    db_item = crud.get_flavor(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Flavor not found")
    return db_item


@db.read_transaction
@router.get("/", response_model=List[schemas.Flavor])
def read_flavors(skip: int = 0, limit: int = 100):
    return crud.get_flavors()[skip : skip + limit]


@db.write_transaction
@router.delete("/{uid}")
def delete_flavors(uid: str) -> bool:
    db_item = crud.get_flavor(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Flavor not found")
    return crud.remove_flavor(db_item)
