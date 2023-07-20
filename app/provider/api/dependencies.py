from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.identity_provider.crud import identity_provider
from app.location.crud import location
from app.provider.crud import provider
from app.provider.models import Provider
from app.provider.schemas_extended import ProviderCreateExtended
from app.service.crud import service
from app.utils import find_duplicates


def valid_provider_id(provider_uid: UUID4) -> Provider:
    item = provider.get(uid=str(provider_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider '{provider_uid}' not found",
        )
    return item


def is_unique_provider(item: ProviderCreateExtended) -> ProviderCreateExtended:
    db_item = provider.get(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Provider with name '{item.name}' already registered",
        )
    return item


def valid_flavor_list(
    item: ProviderCreateExtended = Depends(is_unique_provider),
) -> ProviderCreateExtended:
    find_duplicates(item.flavors, "name")
    find_duplicates(item.flavors, "uuid")
    return item


def valid_image_list(
    item: ProviderCreateExtended = Depends(valid_flavor_list),
) -> ProviderCreateExtended:
    find_duplicates(item.images, "name")
    find_duplicates(item.images, "uuid")
    return item


def valid_project_list(
    item: ProviderCreateExtended = Depends(valid_image_list),
) -> ProviderCreateExtended:
    find_duplicates(item.projects, "name")
    find_duplicates(item.projects, "uuid")
    return item


def valid_service_list(
    item: ProviderCreateExtended = Depends(valid_project_list),
) -> ProviderCreateExtended:
    find_duplicates(item.services, "endpoint")
    for i in item.services:
        db_item = service.get(endpoint=i.endpoint)
        if db_item is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service with URL '{i.endpoint}' already registered",
            )
    return item


def valid_identity_provider_list(
    item: ProviderCreateExtended = Depends(valid_service_list),
) -> ProviderCreateExtended:
    find_duplicates(item.identity_providers, "endpoint")
    for i in item.identity_providers:
        db_item = identity_provider.get(endpoint=i.endpoint)
        if db_item is not None:
            for k, v in i.dict(exclude={"relationship"}).items():
                if db_item.__getattribute__(k) != v:
                    msg = f"Identity Provider with URL '{i.endpoint}' "
                    msg += "already exists, but with different attributes. "
                    msg += f"Received: {i.dict()}. Stored: {db_item}"
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=msg
                    )
    return item


def valid_location(
    item: ProviderCreateExtended = Depends(valid_identity_provider_list),
) -> ProviderCreateExtended:
    loc = item.location
    if loc is not None:
        db_item = location.get(name=loc.name)
        if db_item is not None:
            for k, v in loc.dict().items():
                if db_item.__getattribute__(k) != v:
                    msg = f"Location with name '{loc.name}' "
                    msg += "already exists, but with different attributes. "
                    msg += f"Received: {loc.dict()}. Stored: {db_item}"
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=msg
                    )
    return item