from fastapi import APIRouter, HTTPException
from neomodel import db
from typing import List

from .. import crud, schemas

router = APIRouter(prefix="/user_groups", tags=["user_groups"])


@db.write_transaction
@router.post("/", response_model=schemas.UserGroup)
def add_user_group(item: schemas.UserGroupCreate):
    db_item = crud.get_user_group(name=item.name)
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_user_group(item)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.UserGroup)
def read_user_group(uid: str):
    db_item = crud.get_user_group(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="UserGroup not found")
    return db_item


@db.read_transaction
@router.get("/", response_model=List[schemas.UserGroup])
def read_user_groups(skip: int = 0, limit: int = 100):
    return crud.get_user_groups()[skip : skip + limit]


@db.write_transaction
@router.delete("/{uid}")
def delete_user_groups(uid: str) -> bool:
    db_item = crud.get_user_group(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="UserGroup not found")
    return crud.remove_user_group(db_item)


@db.write_transaction
@router.post("/{uid}/projects", response_model=schemas.Project)
def add_project_to_user_group(uid: str, item: schemas.ProjectCreate):
    db_user_group = crud.get_user_group(uid=uid)
    if db_user_group is None:
        raise HTTPException(status_code=404, detail="UserGroup not found")
    db_project = crud.create_project(item=item)
    if not crud.connect_project_to_user_group(
        user_group=db_user_group, project=db_project
    ):
        raise HTTPException(
            status_code=500, detail="Relationship creation failed"
        )
    return db_project
