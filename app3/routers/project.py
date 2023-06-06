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


@db.write_transaction
@router.post("/{uid}/flavors", response_model=schemas.Flavor)
def add_flavor_to_project(uid: str, item: schemas.FlavorCreate):
    db_project = crud.get_project(uid=uid)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db_flavor = crud.create_flavor(item=item)
    if not crud.connect_flavor_to_project(
        project=db_project, flavor=db_flavor
    ):
        raise HTTPException(
            status_code=500, detail="Relationship creation failed"
        )
    return db_flavor


@db.write_transaction
@router.post("/{uid}/images", response_model=schemas.Image)
def add_image_to_project(uid: str, item: schemas.ImageCreate):
    db_project = crud.get_project(uid=uid)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db_image = crud.create_image(item=item)
    if not crud.connect_image_to_project(project=db_project, image=db_image):
        raise HTTPException(
            status_code=500, detail="Relationship creation failed"
        )
    return db_image
