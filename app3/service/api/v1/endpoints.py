from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_service_id
from ...crud import service
from ...models import Service as ServiceModel
from ...schemas import Service, ServiceQuery, ServiceUpdate
from ....identity_provider.schemas import IdentityProvider
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/services", tags=["services"])


@db.read_transaction
@router.get("/", response_model=List[Service])
def get_services(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ServiceQuery = Depends(),
):
    items = service.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{service_uid}", response_model=Service)
def get_service(item: ServiceModel = Depends(valid_service_id)):
    return item


@db.write_transaction
@router.put("/{service_uid}", response_model=Optional[Service])
def put_service(
    update_data: ServiceUpdate,
    item: ServiceModel = Depends(valid_service_id),
):
    return service.update(old_item=item, new_item=update_data)


@db.write_transaction
@router.delete("/{service_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_services(item: ServiceModel = Depends(valid_service_id)):
    if not service.remove(item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.read_transaction
@router.get(
    "/{service_uid}/identity_providers", response_model=List[IdentityProvider]
)
def read_user_group_services(
    item: ServiceModel = Depends(valid_service_id),
):
    return item.provider.single().identity_providers.all()
