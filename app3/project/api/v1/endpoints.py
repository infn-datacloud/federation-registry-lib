from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_project_id
from ...crud import project
from ...models import Project as ProjectModel
from ...schemas import Project, ProjectQuery, ProjectUpdate
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/projects", tags=["projects"])


@db.read_transaction
@router.get("/", response_model=List[Project])
def get_projects(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ProjectQuery = Depends(),
):
    items = project.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{project_uid}", response_model=Project)
def get_project(item: ProjectModel = Depends(valid_project_id)):
    return item


@db.write_transaction
@router.put("/{project_uid}", response_model=Optional[Project])
def put_project(
    update_data: ProjectUpdate, item: ProjectModel = Depends(valid_project_id)
):
    return project.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{project_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(item: ProjectModel = Depends(valid_project_id)):
    if not project.remove(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
