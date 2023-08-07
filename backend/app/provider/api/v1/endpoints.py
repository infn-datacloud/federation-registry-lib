from fastapi import APIRouter, Depends, HTTPException, Response, status
from neomodel import db
from typing import List, Optional, Union
from app.auth_method.schemas import AuthMethodCreate, AuthMethodUpdate

from app.identity_provider.api.dependencies import valid_identity_provider_id
from app.identity_provider.models import IdentityProvider
from app.location.api.dependencies import valid_location_id
from app.location.models import Location
from app.pagination import Pagination, paginate
from app.provider.api.dependencies import (
    is_unique_provider,
    valid_flavor_list,
    valid_identity_provider_list,
    valid_image_list,
    valid_project_list,
    valid_provider_id,
    valid_location,
    valid_service_list,
    validate_new_provider_values,
)
from app.provider.crud import provider
from app.provider.models import Provider
from app.provider.schemas import ProviderQuery
from app.provider.schemas_extended import (
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderUpdate,
)
from app.query import CommonGetQuery

router = APIRouter(prefix="/providers", tags=["providers"])


@db.read_transaction
@router.get("/", response_model=List[ProviderReadExtended])
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
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProviderReadExtended,
    dependencies=[
        Depends(is_unique_provider),
        Depends(valid_flavor_list),
        Depends(valid_identity_provider_list),
        Depends(valid_image_list),
        Depends(valid_location),
        Depends(valid_project_list),
        Depends(valid_service_list),
    ],
)
def post_provider(item: ProviderCreateExtended):
    return provider.create(obj_in=item, force=True)


@db.read_transaction
@router.get("/{provider_uid}", response_model=ProviderReadExtended)
def get_provider(item: Provider = Depends(valid_provider_id)):
    return item


@db.write_transaction
@router.put(
    "/{provider_uid}",
    response_model=Optional[ProviderReadExtended],
    dependencies=[Depends(validate_new_provider_values)],
)
def put_provider(
    update_data: ProviderUpdate,
    response: Response,
    item: Provider = Depends(valid_provider_id),
):
    db_item = provider.update(db_obj=item, obj_in=update_data)
    if db_item is None:
        response.status_code = status.HTTP_304_NOT_MODIFIED
    return db_item


@db.write_transaction
@router.delete("/{provider_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_providers(item: Provider = Depends(valid_provider_id)):
    if not provider.remove(db_obj=item):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )


@db.write_transaction
@router.put(
    "/{provider_uid}/identity_providers/{identity_provider_uid}", response_model=ProviderReadExtended
)
def connect_provider_to_identity_providers(
    data: Union[AuthMethodCreate, AuthMethodUpdate],
    response: Response,
    item: Provider = Depends(valid_provider_id),
    identity_provider: IdentityProvider = Depends(valid_identity_provider_id),
):
    if item.identity_providers.is_connected(identity_provider):
        db_item = item.identity_providers.relationship(identity_provider)
        if all(
            [
                db_item.__getattribute__(k) == v
                for k, v in data.dict(exclude_unset=True).items()
            ]
        ):
            response.status_code = status.HTTP_304_NOT_MODIFIED
            return None
        item.identity_providers.disconnect(identity_provider)
    item.identity_providers.connect(identity_provider, data.dict())
    return item


@db.write_transaction
@router.delete(
    "/{provider_uid}/identity_providers/{identity_provider_uid}", response_model=ProviderReadExtended
)
def disconnect_provider_from_identity_providers(
    response: Response,
    item: Provider = Depends(valid_provider_id),
    identity_provider: IdentityProvider = Depends(valid_identity_provider_id),
):
    if not item.identity_providers.is_connected(identity_provider):
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return None
    item.identity_providers.disconnect(identity_provider)
    return item


@db.write_transaction
@router.put("/{provider_uid}/locations/{location_uid}", response_model=ProviderReadExtended)
def connect_provider_to_location(
    response: Response,
    item: Provider = Depends(valid_provider_id),
    location: Location = Depends(valid_location_id),
):
    if item.location.single() is None:
        item.location.connect(location)
    elif not item.location.is_connected(location):
        item.location.replace(location)
    else:
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return None
    return item


@db.write_transaction
@router.delete(
    "/{provider_uid}/locations/{location_uid}", response_model=ProviderReadExtended
)
def disconnect_provider_from_location(
    response: Response,
    item: Provider = Depends(valid_provider_id),
    location: Location = Depends(valid_location_id),
):
    if not item.location.is_connected(location):
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return None
    item.location.disconnect(location)
    return item
