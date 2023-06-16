from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List
from uuid import UUID

from .utils import CommonGetQuery, Pagination, paginate
from .. import crud, schemas

router = APIRouter(prefix="/providers", tags=["providers"])


@db.write_transaction
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Provider
)
def add_provider(item: schemas.ProviderCreate):
    db_item = crud.get_provider(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider already registered",
        )
    return crud.create_provider(item)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Provider)
def read_provider(uid: UUID):
    db_item = crud.get_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found"
        )
    return db_item


@db.write_transaction
@router.patch("/{uid}", response_model=schemas.Provider)
def update_provider(uid: UUID, item: schemas.ProviderUpdate):
    db_item = crud.get_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found"
        )
    return crud.update_provider(old_item=db_item, new_item=item)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_providers(uid: UUID):
    db_item = crud.get_provider(uid=str(uid).replace("-", ""))
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found"
        )
    if not crud.remove_provider(db_item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get("/", response_model=List[schemas.Provider])
def read_providers(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.UserGroupBase = Depends(),
):
    items = crud.get_providers(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


# @db.write_transaction
# @router.post(
#    "/{uid}/images",
#    response_model=Tuple[schemas.Image, schemas.SupportedImage],
# )
# def connect_image_to_provider(
#    uid: str,
#    item: schemas.ImageCreate,
#    relationship: schemas.SupportedImageCreate,
# ):
#    linked_node = crud.get_provider(uid=uid)
#    if linked_node is None:
#        raise HTTPException(status_code=404, detail="Provider not found")
#    db_item = crud.get_image(**item.dict(exclude_unset=True))
#    if db_item is None:
#        db_item = crud.create_image(item)
#        rel = db_item.provider.connect(linked_node, relationship.dict())
#        return (db_item, rel)
#    elif db_item.provider.relationship(linked_node) is None:
#        raise HTTPException(
#            status_code=400,
#            detail="Image already registered, but not connected",
#        )
#    else:
#        raise HTTPException(status_code=400, detail="Image already registered")
#
#
# @db.write_transaction
# @router.patch("/{uid}/images", response_model=schemas.SupportedImage)
# def update_image_provider_connection(
#    uid: str,
#    image_id: str,
#    relationship: schemas.SupportedImageCreate,
# ):
#    linked_node = crud.get_provider(uid=uid)
#    if linked_node is None:
#        raise HTTPException(status_code=404, detail="Provider not found")
#    db_item = crud.get_image(uid=image_id)
#    if db_item is None:
#        raise HTTPException(status_code=404, detail="Image not found")
#
#    if db_item.provider.relationship(linked_node) is not None:
#        db_item.provider.disconnect(linked_node)
#    return db_item.provider.connect(linked_node, relationship.dict())


# @db.write_transaction
# @router.delete("/{uid}/images", response_model=bool)
# def delete_image_provider_connection(
#    uid: str, relationship_id: str, item: schemas.ImageCreate
# ):
#    linked_node = crud.get_provider(uid=uid)
#    if linked_node is None:
#        raise HTTPException(status_code=404, detail="Provider not found")
#    db_item = crud.get_image(uid=image_id)
#    if db_item is None:
#        raise HTTPException(status_code=404, detail="Image not found")
#
#    if db_item.provider.relationship(linked_node) is None:
#        raise HTTPException(status_code=404, detail="Relationship not found")
#    db_item.provider.disconnect(linked_node)
#    return True
#
