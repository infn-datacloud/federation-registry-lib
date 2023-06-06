from uuid import UUID
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/flavors", tags=["flavors"])


@router.get("/{id}", response_model=schemas.Flavor)
def read_flavor(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_flavor, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="Flavor not found")
        return item


@router.get("/", response_model=List[schemas.Flavor])
def read_flavors(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
):
    with db.session() as session:
        return session.execute_read(crud.get_flavors)


@router.delete("/{id}")
def delete_flavors(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_flavor, id=id)
