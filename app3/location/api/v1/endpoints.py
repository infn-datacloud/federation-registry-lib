from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_location_id
from ...crud import location
from ...models import Location as LocationModel
from ...schemas import Location, LocationQuery, LocationUpdate
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/locations", tags=["locations"])


@db.read_transaction
@router.get("/", response_model=List[Location])
def get_locations(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: LocationQuery = Depends(),
):
    items = location.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{location_uid}", response_model=Location)
def get_location(item: LocationModel = Depends(valid_location_id)):
    return item


@db.write_transaction
@router.put("/{location_uid}", response_model=Optional[Location])
def put_location(
    update_data: LocationUpdate,
    item: LocationModel = Depends(valid_location_id),
):
    return location.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{location_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(item: LocationModel = Depends(valid_location_id)):
    if not location.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
