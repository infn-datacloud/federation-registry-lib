from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from ..schemas_extended import ProviderCreateExtended
from ..models import Provider
from ..crud import provider
from ...service.api.dependencies import is_unique_service


def valid_provider_id(provider_uid: UUID4) -> Provider:
    item = provider.get(uid=str(provider_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider {provider_uid} not found",
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


def check_valid_services(
    item: ProviderCreateExtended = Depends(is_unique_provider),
) -> ProviderCreateExtended:
    for s in item.services:
        is_unique_service(s)
    return item


def check_rel_consistency(
    item: ProviderCreateExtended = Depends(check_valid_services),
) -> ProviderCreateExtended:
    for i in [item.clusters, item.flavors, item.images, item.projects]:
        seen = set()
        names = [j.name for j in i]
        dupes = [x for x in names if x in seen or seen.add(x)]
        duplicates = ",".join(dupes)
        if len(dupes) > 0:
            msg = "There are multiple items with identical name: "
            msg += f"{duplicates}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg,
            )
        seen = set()
        uuids = [j.uuid for j in i]
        dupes = [str(x) for x in uuids if x in seen or seen.add(x)]
        duplicates = ",".join(dupes)
        if len(dupes) > 0:
            msg = "There are multiple items with identical uuid: "
            msg += f"{duplicates}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg,
            )
    return item
