from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/images", tags=["images"])


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Image)
def read_image(uid: UUID):
    db_item = crud.get_image(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Image])
def update_image(uid: UUID, item: schemas.ImageUpdate):
    db_item = crud.get_image(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return crud.update_image(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_images(uid: UUID):
    db_item = crud.get_image(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    if not crud.remove_image(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.Image])
def read_images(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.ImageBase = Depends(),
):
    items = crud.get_images(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )

    return paginate(items=items, page=page.page, size=page.size)
