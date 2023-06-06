from fastapi import APIRouter, HTTPException
from neomodel import db
from typing import List

from .. import crud, schemas

router = APIRouter(prefix="/images", tags=["images"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Image)
def read_image(uid: str):
    db_item = crud.get_image(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_item


@db.read_transaction
@router.get("/", response_model=List[schemas.Image])
def read_images(skip: int = 0, limit: int = 100):
    return crud.get_images()[skip : skip + limit]


@db.write_transaction
@router.delete("/{uid}")
def delete_images(uid: str) -> bool:
    db_item = crud.get_image(uid=uid)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return crud.remove_image(db_item)
