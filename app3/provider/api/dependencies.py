from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from ..schemas_extended import ProviderCreateExtended
from ..models import Provider
from ..crud import provider
from ...service_type.api.dependencies import valid_service_type_name
from ...service.schemas_extended import ServiceCreateExtended


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


def check_rel_consistency(
    item: ProviderCreateExtended = Depends(is_unique_provider),
) -> ProviderCreateExtended:
    for l in [item.clusters, item.flavors, item.images, item.projects]:
        names = [i.relationship.name for i in l]
        if len(names) != len(set(names)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"There are multiple items with the same relationship name",
            )
        uuids = [i.relationship.uuid for i in l]
        if len(uuids) != len(set(uuids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"There are multiple items with the same relationship uuid",
            )
    return item


def check_valid_services(
    item: ProviderCreateExtended = Depends(check_rel_consistency),
) -> ProviderCreateExtended:
    for s in item.services:
        valid_service_type_name(s.type)
    return item


# def check_rel_uniqueness(
#    item: ProviderCreateExtended,
# ) -> ProviderCreateExtended:
#    for l in [item.clusters, item.flavors, item.images, item.projects]:
#        for i in l:
#            end_node_rel_match_name = l.match(name=i.relationship.name).all()
#            if len(end_node_rel_match_name) > 1:
#                raise HTTPException(
#                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                    detail=f"There are multiple items with relationship matching name '{i.relationship.name}'",
#                )
#            elif len(end_node_rel_match_name) == 1:
#                end_node_rel_match_name = end_node_rel_match_name[0]
#            else:
#                end_node_rel_match_name = None
#
#            end_node_rel_match_uuid = l.match(uuid=i.relationship.uuid).all()
#            if len(end_node_rel_match_uuid) > 1:
#                raise HTTPException(
#                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                    detail=f"There are multiple items with relationship matching uuid '{i.relationship.uuid}'",
#                )
#            elif len(end_node_rel_match_uuid) == 1:
#                end_node_rel_match_uuid = end_node_rel_match_uuid[0]
#            else:
#                end_node_rel_match_uuid = None
#    return item
#
