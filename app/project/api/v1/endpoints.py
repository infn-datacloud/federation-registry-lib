from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from app.flavor.api.dependencies import valid_flavor_id
from app.flavor.models import Flavor as FlavorModel
from app.image.api.dependencies import valid_image_id
from app.image.models import Image as ImageModel
from app.project.api.dependencies import valid_project_id
from app.project.crud import project
from app.project.models import Project as ProjectModel
from app.project.schemas import ProjectQuery, ProjectRead, ProjectUpdate
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery

router = APIRouter(prefix="/projects", tags=["projects"])


@db.read_transaction
@router.get("/", response_model=List[ProjectRead])
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
@router.get("/{project_uid}", response_model=ProjectRead)
def get_project(item: ProjectModel = Depends(valid_project_id)):
    return item


@db.write_transaction
@router.put("/{project_uid}", response_model=Optional[ProjectRead])
def put_project(
    update_data: ProjectUpdate, item: ProjectModel = Depends(valid_project_id)
):
    return project.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{project_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(item: ProjectModel = Depends(valid_project_id)):
    if not project.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.write_transaction
@router.put("/{user_group_uid}/flavors", response_model=ProjectRead)
def connect_user_group_flavor(
    item: ProjectModel = Depends(valid_project_id),
    flavor: FlavorModel = Depends(valid_flavor_id),
):
    item.flavors.connect(flavor)
    return item


@db.read_transaction
@router.delete("/{user_group_uid}/flavors", response_model=ProjectRead)
def disconnect_user_group_flavor(
    item: ProjectModel = Depends(valid_project_id),
    flavor: FlavorModel = Depends(valid_flavor_id),
):
    item.flavors.disconnect(flavor)
    return item


@db.write_transaction
@router.put("/{project_uid}/images", response_model=ProjectRead)
def connect_user_group_images_link(
    item: ProjectModel = Depends(valid_project_id),
    image: ImageModel = Depends(valid_image_id),
):
    item.images.connect(image)
    return item


@db.read_transaction
@router.delete("/{project_uid}/images", response_model=ProjectRead)
def disconnect_user_group_images_link(
    item: ProjectModel = Depends(valid_project_id),
    image: ImageModel = Depends(valid_image_id),
):
    item.images.disconnect(image)
    return item
