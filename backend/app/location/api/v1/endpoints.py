from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db
from typing import List, Optional

from app.location.api.dependencies import (
    validate_new_location_values,
    valid_location_id,
)
from app.location.crud import location
from app.location.models import Location
from app.location.schemas import LocationQuery, LocationUpdate
from app.location.schemas_extended import LocationReadExtended
from app.pagination import Pagination, paginate
from app.query import CommonGetQuery

router = APIRouter(prefix="/locations", tags=["locations"])


@db.read_transaction
@router.get("/", response_model=List[LocationReadExtended])
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
@router.get("/{location_uid}", response_model=LocationReadExtended)
def get_location(item: Location = Depends(valid_location_id)):
    return item


@db.write_transaction
@router.put(
    "/{location_uid}",
    response_model=Optional[LocationReadExtended],
    dependencies=[Depends(validate_new_location_values)],
)
def put_location(
    update_data: LocationUpdate,
    response: Response,
    item: Location = Depends(valid_location_id),
):
    db_item = location.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete("/{location_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(item: Location = Depends(valid_location_id)):
    if not location.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
