from uuid import UUID
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/user_groups", tags=["user_groups"])


@router.post("/", response_model=schemas.UserGroup)
def add_user_group(item: schemas.UserGroupCreate):
    with db.session() as session:
        db_user_group = session.execute_read(
            crud.get_user_group_by_name, name=item.name
        )
        if db_user_group:
            raise HTTPException(
                status_code=400, detail="Name already registered"
            )
        return session.execute_write(crud.create_user_group, **item.dict())


@router.get("/{id}", response_model=schemas.UserGroup)
def read_user_group(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_user_group, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="UserGroup not found")
        return item


@router.get("/", response_model=List[schemas.UserGroup])
def read_user_groups(
    skip: int = 0,
    limit: int = 100,
    user_group_id: Optional[int] = None,
):
    with db.session() as session:
        return session.execute_read(crud.get_user_groups)


@router.delete("/{id}")
def delete_user_groups(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_user_group, id=id)


@router.post("/{user_group_id}/projects", response_model=schemas.Project)
def add_project(user_group_id: UUID, item: schemas.ProjectCreate):
    with db.session() as session:
        return session.execute_write(
            crud.create_project, user_group_id=user_group_id, **item.dict()
        )
