from fastapi import HTTPException, status
from pydantic import UUID4
from typing import Callable, Mapping

from ... import crud


class CheckItemExists:
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


valid_cluster_id = CheckItemExists("Cluster", crud.get_cluster)
valid_flavor_id = CheckItemExists("Flavor", crud.get_flavor)
valid_identity_provider_id = CheckItemExists(
    "IdentityProvider", crud.get_identity_provider
)
valid_image_id = CheckItemExists("Image", crud.get_image)
valid_location_id = CheckItemExists("Location", crud.get_location)
valid_project_id = CheckItemExists("Project", crud.get_project)
valid_provider_id = CheckItemExists("Provider", crud.get_provider)
valid_quota_id = CheckItemExists("Quota", crud.get_quota)
valid_quota_type_id = CheckItemExists("QuotaType", crud.get_quota_type)
valid_service_id = CheckItemExists("Service", crud.get_service)
valid_service_type_id = CheckItemExists("serviceType", crud.get_service_type)
valid_sla_id = CheckItemExists("SLA", crud.get_sla)
valid_user_group_id = CheckItemExists("UserGroup", crud.get_user_group)
