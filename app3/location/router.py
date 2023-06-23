from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .crud import edit_location, read_locations, remove_location
from .dependencies import valid_location_id
from .schemas import Location, LocationPatch, LocationQuery
from ..pagination import Pagination, paginate
from ..query import CommonGetQuery

router = APIRouter(prefix="/locations", tags=["locations"])


@db.read_transaction
@router.get("/", response_model=List[Location])
def get_locations(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: LocationQuery = Depends(),
):
    items = read_locations(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{location_uid}", response_model=Location)
def get_location(item: Mapping = Depends(valid_location_id)):
    return item


@db.write_transaction
@router.patch("/{location_uid}", response_model=Optional[Location])
def patch_location(
    update_data: LocationPatch, item: Mapping = Depends(valid_location_id)
):
    return edit_location(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{location_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(item: Mapping = Depends(valid_location_id)):
    if not remove_location(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
