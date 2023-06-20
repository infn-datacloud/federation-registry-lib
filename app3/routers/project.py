from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_project_id
from .. import crud, schemas

router = APIRouter(prefix="/projects", tags=["projects"])


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


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Project)
def read_project(item: Mapping = Depends(valid_project_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Project])
def update_project(
    update_data: schemas.ProjectUpdate,
    item: Mapping = Depends(valid_project_id),
):
    return crud.update_project(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(item: Mapping = Depends(valid_project_id)):
    if not crud.remove_project(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
