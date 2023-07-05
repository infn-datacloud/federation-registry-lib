from fastapi import APIRouter, Depends, HTTPException, status
from neomodel import db
from typing import List, Optional

from ..dependencies import valid_service_type_id, is_unique_service_type
from ...crud import service_type
from ...models import ServiceType as ServiceTypeModel
from ...schemas import ServiceTypeQuery, ServiceTypeUpdate
from ...schemas_extended import ServiceTypeCreateExtended, ServiceTypeExtended
from ....pagination import Pagination, paginate
from ....query import CommonGetQuery

router = APIRouter(prefix="/service_types", tags=["service_types"])


@db.write_transaction
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceTypeExtended,
)
def post_service_type(
    item: ServiceTypeCreateExtended = Depends(is_unique_service_type),
):
    return service_type.create_with_quotas(obj_in=item)


@db.read_transaction
@router.get("/", response_model=List[ServiceTypeExtended])
def get_service_types(
    comm: CommonGetQuery = Depends(),
    page: Pagination = Depends(),
    item: ServiceTypeQuery = Depends(),
):
    items = service_type.get_multi(
        **comm.dict(exclude_none=True), **item.dict(exclude_none=True)
    )
    return paginate(items=items, page=page.page, size=page.size)


@db.read_transaction
@router.get("/{service_type_uid}", response_model=ServiceTypeExtended)
def get_service_type(item: ServiceTypeModel = Depends(valid_service_type_id)):
    return item


@db.write_transaction
@router.put(
    "/{service_type_uid}", response_model=Optional[ServiceTypeExtended]
)
def put_service_type(
    update_data: ServiceTypeUpdate,
    item: ServiceTypeModel = Depends(valid_service_type_id),
):
    return service_type.update(db_obj=item, obj_in=update_data)


@db.write_transaction
@router.delete("/{service_type_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_types(
    item: ServiceTypeModel = Depends(valid_service_type_id),
):
    if not service_type.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
