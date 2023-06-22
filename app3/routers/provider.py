from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Mapping

from .utils import CommonGetQuery, Pagination, paginate
from .utils.validation import valid_provider_id, check_rel_consistency
from ..schemas import Provider, ProviderCreate, ProviderPatch, ProviderQuery
from ..crud.provider import (
    create_provider,
    edit_provider,
    read_providers,
    remove_provider,
)

router = APIRouter(prefix="/providers", tags=["providers"])


@db.read_transaction
@router.get("/", response_model=List[Provider])
def get_providers(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ProviderQuery = Depends(),
):
    items = read_providers(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Provider)
def post_provider(item: ProviderCreate = Depends(check_rel_consistency)):
    return create_provider(item)


@db.read_transaction
@router.get("/{uid}", response_model=Provider)
def get_provider(item: Mapping = Depends(valid_provider_id)):
    return item


@db.write_transaction
@router.patch("/{uid}", response_model=Provider)
def patch_provider(
    update_data: ProviderPatch, item: Mapping = Depends(valid_provider_id)
):
    return edit_provider(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_providers(item: Mapping = Depends(valid_provider_id)):
    if not remove_provider(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
