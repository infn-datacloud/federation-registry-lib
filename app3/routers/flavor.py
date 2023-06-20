from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_flavor_id
from .. import crud, schemas

router = APIRouter(prefix="/flavors", tags=["flavors"])


@db.read_transaction
@router.get("/", response_model=List[schemas.Flavor])
def read_flavors(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: schemas.FlavorBase = Depends(),
):
    items = crud.get_flavors(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{uid}", response_model=schemas.Flavor)
def read_flavor(item: Mapping = Depends(valid_flavor_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[schemas.Flavor])
def update_flavor(
    update_data: schemas.FlavorUpdate, item: Mapping = Depends(valid_flavor_id)
):
    return crud.update_flavor(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flavors(item: Mapping = Depends(valid_flavor_id)):
    if not crud.remove_flavor(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
