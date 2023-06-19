from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/projects", tags=["projects"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Project)
def read_project(uid: UUID):
    db_item = crud.get_project(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Project])
def update_project(uid: UUID, item: schemas.ProjectUpdate):
    db_item = crud.get_project(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return crud.update_project(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(uid: UUID):
    db_item = crud.get_project(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    if not crud.remove_project(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.Project])
def read_projects(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.ProjectBase = Depends(),
):
    items = crud.get_projects(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)
