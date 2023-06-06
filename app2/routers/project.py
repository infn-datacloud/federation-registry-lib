from uuid import UUID
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/{id}", response_model=schemas.Project)
def read_project(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_project, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return item


@router.get("/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
):
    with db.session() as session:
        return session.execute_read(crud.get_projects)


@router.delete("/{id}")
def delete_projects(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_project, id=id)


@router.post("/{project_id}/flavors", response_model=schemas.Flavor)
def add_flavor(project_id: UUID, item: schemas.FlavorCreate):
    with db.session() as session:
        db_flavor = session.execute_read(
            crud.get_flavor_by_name, name=item.name
        )
        if db_flavor:
            raise HTTPException(
                status_code=400, detail="Name already registered"
            )
        return session.execute_write(
            crud.create_flavor, project_id=project_id, **item.dict()
        )


@router.post("/{project_id}/images", response_model=schemas.Image)
def add_image(project_id: UUID, item: schemas.ImageCreate):
    with db.session() as session:
        db_image = session.execute_read(crud.get_image_by_name, name=item.name)
        if db_image:
            raise HTTPException(
                status_code=400, detail="Name already registered"
            )
        return session.execute_write(
            crud.create_image, project_id=project_id, **item.dict()
        )
