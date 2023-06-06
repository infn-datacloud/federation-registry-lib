from uuid import UUID
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{id}", response_model=schemas.Image)
def read_image(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_image, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="Image not found")
        return item

@router.get("/", response_model=List[schemas.Image])
def read_images(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
):
    with db.session() as session:
        return session.execute_read(crud.get_images)


@router.delete("/{id}")
def delete_images(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_image, id=id)
