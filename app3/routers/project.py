from fastapi import APIRouter, HTTPException
from neomodel import db
from typing import List

from .. import crud, schemas

router = APIRouter(prefix="/projects", tags=["projects"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Project)
def read_project(uid: str):
    db_item = crud.get_project(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_item


@db.read_transaction
@router.get("/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100):
    return crud.get_projects()[skip : skip + limit]


@db.write_transaction
@router.delete("/{uid}")
def delete_projects(uid: str) -> bool:
    db_item = crud.get_project(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.remove_project(db_item)
