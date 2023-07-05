from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List

from ..dependencies import valid_provider_id, check_rel_consistency
from ...crud import provider
from ...models import Provider as ProviderModel
from ...schemas import ProviderQuery
from ...schemas_extended import (
    ProviderCreateExtended,
    ProviderExtended,
    ProviderUpdate,
)
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/providers", tags=["providers"])


@db.read_transaction
@router.get("/", response_model=List[ProviderExtended])
def get_providers(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ProviderQuery = Depends(),
):
    items = provider.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.write_transaction
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ProviderExtended
)
def post_provider(
    item: ProviderCreateExtended = Depends(check_rel_consistency),
):
    return provider.create_with_all(obj_in=item)


@db.read_transaction
@router.get("/{provider_uid}", response_model=ProviderExtended)
def get_provider(item: ProviderModel = Depends(valid_provider_id)):
    return item


@db.write_transaction
@router.put("/{provider_uid}", response_model=ProviderExtended)
def put_provider(
    update_data: ProviderUpdate,
    item: ProviderModel = Depends(valid_provider_id),
):
    return provider.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{provider_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_providers(item: ProviderModel = Depends(valid_provider_id)):
    if not provider.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
