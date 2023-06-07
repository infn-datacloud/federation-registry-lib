from fastapi import APIRouter, HTTPException
from neomodel import db
from typing import List

from .. import crud, schemas

router = APIRouter(prefix="/services", tags=["services"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Service)
def read_service(uid: str):
    db_item = crud.get_service(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_item


@db.read_transaction
@router.get("/", response_model=List[schemas.Service])
def read_services(skip: int = 0, limit: int = 100):
    return crud.get_services()[skip : skip + limit]


@db.write_transaction
@router.delete("/{uid}")
def delete_services(uid: str) -> bool:
    db_item = crud.get_service(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return crud.remove_service(db_item)
