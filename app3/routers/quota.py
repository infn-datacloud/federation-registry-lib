from fastapi import APIRouter, HTTPException
from neomodel import db
from typing import List

from .. import crud, schemas

router = APIRouter(prefix="/quotas", tags=["quotas"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Quota)
def read_quota(uid: str):
    db_item = crud.get_quota(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Quota not found")
    return db_item


@db.read_transaction
@router.get("/", response_model=List[schemas.Quota])
def read_quotas(skip: int = 0, limit: int = 100):
    return crud.get_quotas()[skip : skip + limit]


@db.write_transaction
@router.delete("/{uid}")
def delete_quotas(uid: str) -> bool:
    db_item = crud.get_quota(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Quota not found")
    return crud.remove_quota(db_item)
