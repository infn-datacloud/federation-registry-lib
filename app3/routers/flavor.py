from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping, Optional

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_flavor_id
from ..schemas import Flavor, FlavorPatch, FlavorQuery
from ..crud.flavor import edit_flavor, read_flavors, remove_flavor

router = APIRouter(prefix="/flavors", tags=["flavors"])


@db.read_transaction
@router.get("/", response_model=List[Flavor])
def get_flavors(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: FlavorQuery = Depends(),
):
    items = read_flavors(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{uid}", response_model=Flavor)
def get_flavor(item: Mapping = Depends(valid_flavor_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Optional[Flavor])
def patch_flavor(
    update_data: FlavorPatch, item: Mapping = Depends(valid_flavor_id)
):
    return edit_flavor(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flavors(item: Mapping = Depends(valid_flavor_id)):
    if not remove_flavor(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
