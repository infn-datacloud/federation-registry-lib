from fastapi import Depends, HTTPException, status
from pydantic import UUID4
from typing import Callable, Mapping

from ... import crud


class CheckItemExist:
    def __init__(self, class_name: str, get_item: Callable):
        self.class_name = class_name
        self.get_item = get_item

    def __call__(self, uid: UUID4) -> Mapping:
        item = self.get_item(uid=str(uid).replace("-", ""))
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.class_name} {uid} not found",
            )
        return item


valid_cluster_id = CheckItemExist("Cluster", crud.cluster.read_cluster)
valid_flavor_id = CheckItemExist("Flavor", crud.flavor.read_flavor)
valid_identity_provider_id = CheckItemExist(
    "IdentityProvider", crud.identity_provider.read_identity_provider
)
valid_image_id = CheckItemExist("Image", crud.image.read_image)
valid_location_id = CheckItemExist("Location", crud.location.read_location)
valid_project_id = CheckItemExist("Project", crud.project.read_project)
valid_provider_id = CheckItemExist("Provider", crud.provider.read_provider)
valid_quota_id = CheckItemExist("Quota", crud.quota.read_quota)
valid_quota_type_id = CheckItemExist(
    "QuotaType", crud.quota_type.read_quota_type
)
valid_service_id = CheckItemExist("Service", crud.service.read_service)
valid_service_type_id = CheckItemExist(
    "serviceType", crud.service_type.read_service_type
)
valid_sla_id = CheckItemExist("SLA", crud.sla.read_sla)
valid_user_group_id = CheckItemExist(
    "UserGroup", crud.user_group.read_user_group
)


from ...schemas.nodes.provider import ProviderCreate
from ...crud.provider import read_provider


def is_unique_provider(item: ProviderCreate) -> ProviderCreate:
    db_item = read_provider(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Provider with name '{item.name}' already registered",
        )
    return item


def check_rel_consistency(
    item: ProviderCreate = Depends(is_unique_provider),
) -> ProviderCreate:
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


from ...schemas.nodes.user_group import UserGroupCreate
from ...crud.user_group import read_user_group


def is_unique_user_group(item: UserGroupCreate) -> UserGroupCreate:
    db_item = read_user_group(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User Group with name '{item.name}' already registered",
        )
    return item


from ...schemas.nodes.service_type import ServiceTypeCreate
from ...crud.service_type import read_service_type


def is_unique_service_type(item: ServiceTypeCreate) -> ServiceTypeCreate:
    db_item = read_service_type(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service Type with name '{item.name}' already registered",
        )
    return item
